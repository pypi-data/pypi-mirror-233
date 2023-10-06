#!/usr/bin/env python
"""
Analysis tool for Zeltron simulations.
"""
# adapted from asoudais, bcerutti & ielmellah
# structured inspired by nonos from gwafflard-fernandez, cmt robert

# import sys
# import argparse
import os
import re
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from typing import List, Optional
from zaapy.config import DEFAULTS

from zaapy.__version__ import __version__
from zaapy.api import GasDataSet, Parameters
from zaapy.parser import (
    init_parser,
    is_set,
    parse_image_format,
    parse_output_number_range,
    parse_range,
    range_converter,
    printProgressBar,
)


def main(argv: Optional[List[str]] = None) -> int:
    pars = init_parser()
    args = vars(pars.parse_args(argv))

    for key in args:
        if not is_set(args[key]):
            args[key] = DEFAULTS.get(key)

    if args.pop("version"):
        print(__version__)
        return 0

    if not is_set(args["vmin"]):
        vmin = None
    else:
        vmin = args["vmin"]

    if not is_set(args["vmax"]):
        vmax = None
    else:
        vmax = args["vmax"]

    if not is_set(args["geom"]):
        raise ValueError("The geometry must be given")
    else:
        geometry = args["geom"]

    if not is_set(args["plane"]):
        plane = None
    else:
        plane = args["plane"]

    if args["ncpu"] > (ncpu := min(args["ncpu"], os.cpu_count())):
        raise ValueError(
            f"Requested {args['ncpu']}, but the runner only has access to {ncpu}."
        )

    if args["cmap"] not in mpl.colormaps():
        raise ValueError(
            f"{args['cmap']} is not a valid colormap, supported colormaps: {mpl.colormaps()} "
        )

    fields = args["field"].split(",")
    if len(fields) >= 2:
        raise ValueError("Can only plot a field at once, reduce to a single field")
    else:
        field = fields[0]

    if not is_set(args["title"]):
        title = args["field"]
    else:
        title = args["title"]

    extent = args["range"]

    datadir = args["datadir"]

    try:
        params = Parameters(directory=datadir)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(exc)
        return 1

    params.countSimuFiles()
    data_files = params.data_files

    available = set()
    for fn in data_files:
        if (num := re.search(r"\d+", fn)) is not None:
            available.add(int(num.group()))

    if args.pop("all"):
        requested = available
    else:
        try:
            requested = set(
                parse_output_number_range(args["on"], maxval=max(available))
            )
        except ValueError as exc:
            print(exc)
            return 1

    if not (toplot := list(requested.intersection(available))):
        print(
            f"No requested output file was found (requested {requested}, found {available})."
        )
        return 1
    args["on"] = toplot

    if (show := args.pop("display")) and len(args["on"]) > 1:
        print("display mode can not be used with multiple images, turning it off.")
        show = False

    if not show:
        try:
            args["format"] = parse_image_format(args["format"])
        except ValueError as exc:
            print(exc)
            return 1

    print("Field plotted: ", args["field"])
    for i, on in enumerate(args["on"]):
        ds = GasDataSet(
            on,
            geometry=geometry,
            directory=datadir,
            wanted_keys=args["field"],
            spec=args["spec"],
        )
        dsop = ds[field]
        dim = len(np.shape(dsop.data))
        if plane is None:
            dsop_dict = dsop.coords.get_attributes
            default_plane = []
            for key, val in dsop_dict.items():
                if type(val) != str and val.shape[0] > 2:
                    default_plane.append(key)
            plane = default_plane

        fig = plt.figure()
        ax = fig.add_subplot(111, polar=False)
        if dim == 1:
            dsop.map(plane[0]).plot(
                fig,
                ax,
                log=args["log"],
                vmin=vmin,
                vmax=vmax,
                title="$%s$" % title,
            )
            akey = dsop.map(plane[0]).dict_plotable["abscissa"]
            avalue = dsop.map(plane[0]).dict_plotable[akey]
            extent = parse_range(extent, dim=dim)
            extent = range_converter(extent, abscissa=avalue, ordinate=np.zeros(2))
            ax.set_xlim(extent[0], extent[1])
        elif dim == 2:
            dsop.map(plane[0], plane[1]).plot(
                fig,
                ax,
                log=args["log"],
                vmin=vmin,
                vmax=vmax,
                cmap=args["cmap"],
                title="$%s$" % title,
            )
            akey = dsop.map(plane[0], plane[1]).dict_plotable["abscissa"]
            okey = dsop.map(plane[0], plane[1]).dict_plotable["ordinate"]
            avalue = dsop.map(plane[0], plane[1]).dict_plotable[akey]
            ovalue = dsop.map(plane[0], plane[1]).dict_plotable[okey]
            extent = parse_range(extent, dim=dim)
            extent = range_converter(
                extent,
                abscissa=avalue,
                ordinate=ovalue,
            )
            ax.set_xlim(extent[0], extent[1])
            ax.set_ylim(extent[2], extent[3])

        # logger.debug("processed the data before plotting.")

        if "x" and "z" in plane:
            ax.set_aspect("equal")

        if show:
            plt.show()
        else:
            #     logger.debug("saving plot: started")
            fmt = args["format"]
            log = args["log"]
            dpi = args["dpi"]
            filename = f"{''.join(plane)}_{field}_{'_log' if log else ''}{on:04d}.{fmt}"
            fig.savefig(filename, bbox_inches="tight", dpi=dpi)
        #     logger.debug("saving plot: finished ({})", filename)

        printProgressBar(
            i + 1,
            len(args["on"]),
            prefix="Progress",
            suffix="Complete",
            length=35,
        )

        plt.close(fig)

        del (ds, dsop)

    return 0


if __name__ == "__main__":
    exit(main())

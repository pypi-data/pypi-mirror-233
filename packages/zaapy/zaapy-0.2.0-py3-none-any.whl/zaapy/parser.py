import numpy as np
import argparse
from typing import Any, List, Optional, Union
from zaapy.config import DEFAULTS


def init_parser() -> argparse.ArgumentParser:
    """
    Read from command line the input arguments which are generic to all plots.

    Args:
        dir:    Folder location for data/.
        i1: First iteration to account for.
        i2: Last iteration to account for (default=i1).
        dt: Time step interval to go from i1 to i2 (dumb if i2=i1)
        IO: Do we read data from Zeltron outputs and save it in local npy file (slower, 1st step) or do we read directly from local npy file (faster, 2nd step)?
        var: file containing variables' name to be read from Zeltron outputs (if IO=load)
        sptm: General Relativity or flat spacetime?
        cmap: Colormap name
        dpi: Image file resolution
        vmin: Min value for the colorbar
        vmax: Max value for the colorbar
        ymin: Min value for the vertical axis
        ymax: Max value for the vertical axis
        xmin: Min value for the horizontal axis
        xmax: Max value for the horizontal axis
        view: Set the projection view for the plot
        save: Allows you to save the figure
        psave: Folder location to save the plot (DEFAULT: "./")

    Returns:
        The generic parser, to which can be added new specific arguments afterwhile in parse().

    Examples:
        >>> python XXX.py -dir ../labas -i1 10 -i2 20 -dt 5 -IO load -var variables.dat -sptm GR
    """

    parser = argparse.ArgumentParser(prog="zapy", description=__doc__)

    parser.add_argument(
        "-dir",
        dest="datadir",
        help=f"location of output files and param files (default: '{DEFAULTS['datadir']}').",
    )

    parser.add_argument(
        "-field",
        type=str,
        help=f"name of field to plot (default: '{DEFAULTS['field']}').",
    )
    parser.add_argument(
        "-geom",
        type=str,
        choices=["spherical", "cartesian"],
        help=f"geometry of the simulation (default: '{DEFAULTS['geom']}').",
        required=True,
    )
    parser.add_argument(
        "-spec",
        type=str,
        help=f"species to load (default: '{DEFAULTS['spec']}').",
    )
    select_group = parser.add_mutually_exclusive_group()
    select_group.add_argument(
        "-on",
        type=int,
        nargs="+",
        help="output number(s) (on) to plot. "
        "This can be a single value or a range (start, end, [step]) where both ends are inclusive. ",
    )
    select_group.add_argument(
        "-all",
        action="store_true",
        help="save an image for every available snapshot (this will force show=False).",
    )
    flag_group = parser.add_argument_group("boolean flags")
    flag_group.add_argument(
        "-log",
        action="store_true",
        default=None,
        help="plot the log10 of the field f, i.e. log(f).",
    )
    parser.add_argument(
        "-range",
        type=str,
        nargs="+",
        help=f"range of matplotlib window (default: {DEFAULTS['range']}), example: x x -2 2",
    )
    parser.add_argument(
        "-vmin",
        type=float,
        help=f"min value (default: {DEFAULTS['vmin']})",
    )
    parser.add_argument(
        "-vmax",
        type=float,
        help=f"max value (default: {DEFAULTS['vmax']})",
    )
    parser.add_argument(
        "-plane",
        type=str,
        nargs="+",
        help=f"abscissa and ordinate of the plane of projection (default: '{DEFAULTS['plane']}'), example: x z",
    )

    parser.add_argument(
        "-cpu",
        "-ncpu",
        dest="ncpu",
        type=int,
        help=f"number of parallel processes (default: {DEFAULTS['ncpu']}).",
    )
    parser.add_argument(
        "-cmap",
        help=f"choice of colormap for the 2D maps (default: '{DEFAULTS['cmap']}').",
    )
    parser.add_argument(
        "-title",
        type=str,
        help=f"name of the field in the colorbar for the 2D maps (default: '{DEFAULTS['title']}').",
    )
    parser.add_argument(
        "-dpi",
        type=int,
        help=f"image file resolution (default: {DEFAULTS['dpi']})",
    )
    parser.add_argument(
        "-fmt",
        "-format",
        dest="format",
        help=f"select output image file format (default: {DEFAULTS['format']})",
    )

    cli_only_group = parser.add_argument_group("CLI-only options")
    cli_action_group = cli_only_group.add_mutually_exclusive_group()
    cli_action_group.add_argument(
        "-d",
        "-display",
        dest="display",
        action="store_true",
        help="open a graphic window with the plot (only works with a single image)",
    )
    cli_action_group.add_argument(
        "-version",
        "--version",
        action="store_true",
        help="show raw version number and exit",
    )

    return parser


def is_set(x: Any) -> bool:
    return x not in (None, "unset")


def parse_range(extent, dim: int):
    if not is_set(extent):
        if dim == 2:
            return (None, None, None, None)
        elif dim == 1:
            return (None, None)
        else:
            raise ValueError("dim has to be 1 or 2.")

    if len(extent) != 2 * dim:
        raise ValueError(
            f"Received sequence `extent` with incorrect size {len(extent)}. Expected exactly {2*dim=} values."
        )
    return tuple(float(i) if i != "x" else None for i in extent)


def range_converter(extent, abscissa: np.ndarray, ordinate: np.ndarray):
    trueextent = [abscissa.min(), abscissa.max(), ordinate.min(), ordinate.max()]
    return tuple(i if i is not None else j for (i, j) in zip(extent, trueextent))


def parse_output_number_range(
    on: Optional[Union[List[int], int, str]], maxval: Optional[int] = None
) -> List[int]:
    if not is_set(on):
        if maxval is None:
            raise ValueError("Can't parse a range from unset values without a max.")
        return [maxval]

    if isinstance(on, int):
        return [on]

    assert isinstance(on, list) and all(isinstance(o, int) for o in on)

    if len(on) > 3:
        raise ValueError(
            f"Can't parse a range from sequence {on} with more than 3 values."
        )
    if len(on) == 1:
        return on

    if on[1] < on[0]:
        raise ValueError("Can't parse a range with max < min.")

    # make the upper boundary inclusive
    on[1] += 1
    ret = list(range(*on))
    if maxval is not None and (max_requested := ret[-1]) > maxval:
        raise ValueError(
            f"No output beyond {maxval} is available, but {max_requested} was requested."
        )
    return ret


def parse_image_format(s: Optional[str]) -> str:
    from matplotlib.backend_bases import FigureCanvasBase

    if not is_set(s):
        return FigureCanvasBase.get_default_filetype()

    assert isinstance(s, str)
    _, _, ext = s.rpartition(".")
    if ext not in (
        available := list(FigureCanvasBase.get_supported_filetypes().keys())
    ):
        raise ValueError(
            f"Received unknown file format '{s}'. "
            f"Available formated are {available}."
        )
    return ext


# Print iterations progress
def printProgressBar(
    iteration,
    total,
    prefix="",
    suffix="",
    decimals=1,
    length=50,
    # fill="█",
    fill="\u26A1",
    printEnd="\r",
):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "--" * (length - filledLength)
    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=printEnd, flush=True)
    # Print New Line on Complete
    if iteration == total:
        print()

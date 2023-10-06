import numpy as np
from pathlib import Path
from matplotlib.ticker import SymmetricalLogLocator
from zaapy.api.from_simulation import Parameters


class Plotable:
    def __init__(self, dict_plotable: dict):
        self.dict_plotable = dict_plotable
        self.data = self.dict_plotable[self.dict_plotable["field2plot"]]
        self.dimension = len(self.data.shape)

    def plot(
        self,
        fig,
        ax,
        *,
        log=False,
        cmap="inferno",
        nbin=None,
        filename=None,
        fmt="png",
        dpi=500,
        title=None,
        unit_conversion=None,
        **kwargs,
    ):
        """
        Plotting function
        Args:
            fig,ax

        """

        data = self.data
        shape = data.shape

        if log:
            data = np.log10(data)

        if self.dimension == 2:
            self.akey = self.dict_plotable["abscissa"]
            self.okey = self.dict_plotable["ordinate"]
            self.avalue = self.dict_plotable[self.akey]
            self.ovalue = self.dict_plotable[self.okey]
            # if np.shape(self.avalue) != shape:
            #     self.avalue = self.avalue[: shape[1], : shape[0]]
            # if np.shape(self.ovalue) != shape:
            #     self.ovalue = self.ovalue[: shape[1], : shape[0]]

            kw = {}
            if (norm := kwargs.get("norm")) is not None:
                if "vmin" in kwargs:
                    norm.vmin = kwargs.pop("vmin")
                if "vmax" in kwargs:
                    norm.vmax = kwargs.pop("vmax")
            else:
                vmin = kwargs.pop("vmin") if "vmin" in kwargs else np.nanmin(data)
                vmax = kwargs.pop("vmax") if "vmax" in kwargs else np.nanmax(data)
                kw.update({"vmin": vmin, "vmax": vmax})

            mag_field_lines = self.dict_plotable["flux_func"]
            mfl_shape = mag_field_lines.shape
            if "levels" in kwargs:
                nlevels = int(kwargs.pop("levels"))
            else:
                nlevels = 10

            if ax.name == "polar":
                im = ax.pcolormesh(
                    self.ovalue,
                    self.avalue,
                    data,
                    cmap=cmap,
                    **kwargs,
                    **kw,
                )
                ax.contour(
                    self.ovalue[: mfl_shape[1], : mfl_shape[0]],
                    self.avalue[: mfl_shape[1], : mfl_shape[0]],
                    mag_field_lines,
                    levels=nlevels,
                )
                ax.set(
                    rlim=(-1e-4 * self.avalue.min(), self.avalue.max()),
                    thetalim=(self.ovalue.min(), self.ovalue.max()),
                    theta_direction=-1,
                    theta_zero_location="N",
                )
                ax.set_xlabel(self.okey)
                ax.set_ylabel(self.akey)
            else:
                im = ax.pcolormesh(
                    self.avalue,
                    self.ovalue,
                    data,
                    cmap=cmap,
                    **kwargs,
                    **kw,
                )
                print("Data shape", np.shape(data))
                print("MFL shape", mfl_shape)
                ax.contour(
                    self.avalue[: mfl_shape[0], : mfl_shape[1]],
                    self.ovalue[: mfl_shape[0], : mfl_shape[1]],
                    mag_field_lines,
                    levels=nlevels,
                    colors="k",
                )
                ax.set(
                    xlim=(self.avalue.min(), self.avalue.max()),
                    ylim=(self.ovalue.min(), self.ovalue.max()),
                )

                ax.set_xlabel(self.akey)
                ax.set_ylabel(self.okey)
            if title is not None:
                # from mpl_toolkits.axes_grid1 import make_axes_locatable

                # divider = make_axes_locatable(ax)
                # cax = divider.append_axes("right", size="5%", pad=0.05)
                # cbar = fig.colorbar(
                #    im, cax=cax, orientation="vertical"
                # )  # , format='%.0e')
                cbar = fig.colorbar(im, orientation="vertical")  # , format='%.0e')
                cbar.set_label(title)

                cb_axis = cbar.ax.yaxis

                if cb_axis.get_scale() == "symlog":
                    # no minor tick is drawn in symlog norms by default
                    # as of matplotlib 3.7.1, see
                    # https://github.com/matplotlib/matplotlib/issues/25994
                    trf = cb_axis.get_transform()
                    cb_axis.set_major_locator(SymmetricalLogLocator(trf))
                    if float(trf.base).is_integer():
                        locator = SymmetricalLogLocator(
                            trf, subs=np.arange(1, trf.base)
                        )
                        cb_axis.set_minor_locator(locator)
            else:
                return im

        if self.dimension == 1:
            vmin = kwargs.pop("vmin") if "vmin" in kwargs else np.nanmin(data)
            vmax = kwargs.pop("vmax") if "vmax" in kwargs else np.nanmax(data)
            self.akey = self.dict_plotable["abscissa"]
            self.avalue = self.dict_plotable[self.akey]
            if "norm" in kwargs:
                # logger.info("norm has no meaning in 1D.")
                kwargs.pop("norm")
            im = ax.plot(
                self.avalue,
                data,
                **kwargs,
            )
            ax.set_ylim(ymin=vmin)
            ax.set_ylim(ymax=vmax)
            ax.set_xlabel(self.akey)
            if title is not None:
                ax.set_ylabel(title)
        if filename is not None:
            fig.savefig(f"{filename}.{fmt}", bbox_inches="tight", dpi=dpi)


class Coordinates:
    """Coordinates class from x1, x2, x3"""

    def __init__(self, directory: str, geometry: str):
        self.directory = Path(directory).joinpath("data/")
        self.geometry = geometry
        # cartesian = ["x", "y", "z"]
        # spherical = ["r", "theta", "phi"]
        if self.geometry not in ["cartesian", "spherical"]:
            raise NotImplementedError(f"{self.geometry} not implemented.")
        # if x1 in cartesian and x2 in spherical or x1 in spherical and x2 in cartesian:
        #    raise ValueError(f"{x1} and {x2} must be from the same geometry")

        if self.geometry == "cartesian":
            if Path(self.directory).joinpath("x.dat").is_file():
                self.x = np.loadtxt(Path(self.directory).joinpath("x.dat"))
            if Path(self.directory).joinpath("y.dat").is_file():
                self.y = np.loadtxt(Path(self.directory).joinpath("y.dat"))
            # if Path(self.directory).joinpath("z.dat").is_file():
            #    self.z = np.loadtxt(Path(self.directory).joinpath("z.dat"))
            self.cube = ("x", "y", "z")
        if self.geometry == "spherical":
            if Path(self.directory).joinpath("r.dat").is_file():
                self.r = np.loadtxt(Path(self.directory).joinpath("r.dat"))
            if Path(self.directory).joinpath("theta.dat").is_file():
                self.theta = np.loadtxt(Path(self.directory).joinpath("theta.dat"))
            # if Path(self.directory).joinpath("phi.dat").is_file():
            #    self.phi = np.loadtxt(Path(self.directory).joinpath("phi.dat"))
            self.cube = ("r", "theta", "phi")

    @property
    def shape(self):
        """
        Returns
        =======
        shape : tuple
        """
        if self.geometry == "cartesian":
            return len(self.x), len(self.y)
        if self.geometry == "spherical":
            return len(self.r), len(self.theta)

    @property
    def get_attributes(self):
        if self.geometry == "cartesian":
            return {"geometry": self.geometry, "x": self.x, "y": self.y}
        if self.geometry == "spherical":
            return {
                "geometry": self.geometry,
                "r": self.r,
                "theta": self.theta,
                # "phi": self.phi,
            }

    @property
    def get_coords(self):
        if self.geometry == "cartesian":
            return {
                "x": self.x,
                "y": self.y,
            }
        if self.geometry == "spherical":
            return {
                "r": self.r,
                "theta": self.theta,
            }

    def _meshgrid_reduction(self, *reducted):
        for i in reducted:
            if i not in self.cube:
                raise KeyError(f"{i} not in {self.cube}")
        dictcoords = {}
        if len(reducted) <= 2:
            for coords in reducted:
                dictcoords[coords] = vars(self)[coords]
            # axis = list(set(reducted) ^ set(self.cube))
            # print(axis)
            dictmesh = {}
            # 2D map
            # if len(axis) == 1:

            dictmesh[reducted[0]], dictmesh[reducted[1]] = np.meshgrid(
                dictcoords[reducted[0]],
                dictcoords[reducted[1]],
                indexing="ij",
            )
            # axismed = "".join([axis[0], "med"])
            # dictmesh[axis[0]] = vars(self)[axismed]
            # carefule: takes "xy", "yz", "zx" (all combinations)

            if "".join(reducted) in "".join((*self.cube, self.cube[0])):
                ordered = True
            else:
                ordered = False
            dictmesh["ordered"] = ordered
            # 1D curve
            # else:
            #    dictmesh[reducted[0]] = vars(self)["".join([reducted[0], "med"])]
        else:
            raise ValueError(f"more than 2 coordinates were specified: {reducted}.")
        return dictmesh

    def native_from_wanted(self, *wanted):
        if self.geometry == "cartesian":
            conversion = {
                "x": "x",
                "y": "y",
                "z": "z",
            }
        if self.geometry == "polar":
            conversion = {
                "R": "R",
                "phi": "phi",
                "z": "z",
                "x": "R",
                "y": "phi",
                "r": "R",
                "theta": "z",
            }
        if self.geometry == "spherical":
            conversion = {
                "r": "r",
                "theta": "theta",
                # "phi": "phi",
                "x": "r",
                # "y": "phi",
                "z": "theta",
                "R": "r",
            }
        for i in wanted:
            if i not in tuple(conversion.keys()):
                raise KeyError(f"{i} not in {tuple(conversion.keys())}")
        if set(wanted) & {"x", "y", "z"} == set(wanted):
            target_geometry = "cartesian"
        elif set(wanted) & {"R", "phi", "z"} == set(wanted):
            #        elif set(wanted) & {"R", "z"} == set(wanted):
            target_geometry = "polar"
        #        elif set(wanted) & {"r", "theta", "phi"} == set(wanted):
        elif set(wanted) & {"r", "theta"} == set(wanted):
            target_geometry = "spherical"
        else:
            raise ValueError(f"Unknown wanted plane: {wanted}.")
        native = tuple(conversion[i] for i in wanted)
        return native, target_geometry

    # for 2D arrays
    def target_from_native(self, target_geometry, coords):
        """
        Returns:
            grid converted to the targeted geometry
        """
        if self.geometry == "polar":
            # R, phi, z = (coords["R"], coords["phi"], coords["z"])
            R, z = (coords["R"], coords["z"])
            if target_geometry == "cartesian":
                # x = R * np.cos(phi)
                # y = R * np.sin(phi)
                # target_coords = {"x": x, "y": y, "z": z}
                target_coords = {"x": R, "z": z}
            elif target_geometry == "spherical":
                r = np.sqrt(R**2 + z**2)
                theta = np.arctan2(R, z)
                target_coords = {"r": r, "theta": theta}  # , "phi": phi}
            else:
                raise ValueError(f"Unknown target geometry {target_geometry}.")

        elif self.geometry == "cartesian":
            x, y, z = (coords["x"], coords["y"], coords["z"])
            if target_geometry == "polar":
                R = np.sqrt(x**2 + y**2)
                phi = np.arctan2(y, x)
                target_coords = {"R": R, "phi": phi}  # , "z": z}
                # raise NotImplementedError(f"Target geometry {target_geometry} not implemented yet.")
            elif target_geometry == "spherical":
                r = np.sqrt(x**2 + y**2 + z**2)
                theta = np.arctan2(np.sqrt(x**2 + y**2), z)
                phi = np.arctan2(y, x)
                target_coords = {"r": r, "theta": theta, "phi": phi}
            else:
                raise ValueError(f"Unknown target geometry {target_geometry}.")

        elif self.geometry == "spherical":
            # r, theta, phi = (coords["r"], coords["theta"], coords["phi"])
            r, theta = (coords["r"], coords["theta"])  # , coords["phi"])
            if target_geometry == "polar":
                R = r * np.sin(theta)
                z = r * np.cos(theta)
                # target_coords = {"R": R, "phi": phi, "z": z}
                target_coords = {"R": R, "z": z}
            elif target_geometry == "cartesian":
                # x = r * np.sin(theta) * np.cos(phi)
                # y = r * np.sin(theta) * np.sin(phi)
                # z = r * np.cos(theta)
                x = r * np.sin(theta)
                z = r * np.cos(theta)
                # if len(theta.shape) <= 1:
                #    x = r * np.sin(theta) * np.cos(phi)
                #    y = r * np.sin(theta) * np.sin(phi)
                #    z = np.cos(theta)
                # target_coords = {"x": x, "y": y, "z": z}
                target_coords = {"x": x, "z": z}
            else:
                raise ValueError(f"Unknown target geometry {target_geometry}.")

        else:
            raise ValueError(f"Unknown geometry {self.geometry}.")
        target_coords["ordered"] = coords["ordered"]
        return target_coords

    def _meshgrid_conversion(self, *wanted):
        """
        Return:
            new meshgrid coords for the wanted geometry
        """
        native_from_wanted = self.native_from_wanted(*wanted)
        native = native_from_wanted[0]
        target_geometry = native_from_wanted[1]
        native_meshcoords = self._meshgrid_reduction(*native)
        if len(wanted) == 1:
            return native_meshcoords
        else:
            meshcoords = {}
            if target_geometry == self.geometry:
                meshcoords = native_meshcoords
            else:
                meshcoords = self.target_from_native(target_geometry, native_meshcoords)
            return meshcoords


class GasField:
    def __init__(
        self,
        field: str,
        data: np.ndarray,
        geometry: str,
        it: int,
        mfl: np.ndarray,
        operation: str = "",
        *,
        directory="",
    ):
        self.field = field
        self.geometry = geometry
        self.data = data
        self.it = it
        self.operation = operation
        self.mfl = mfl
        self.directory = directory
        self.coords = Coordinates(self.directory, self.geometry)

    def map(self, *wanted, x1norm: float = 1.0, x2norm: float = 1.0) -> Plotable:
        data_key = self.field
        if x1norm == 0.0:
            raise ValueError(f"Cannot normalize abscissa axis by {x1norm}")
        if x2norm == 0.0:
            raise ValueError(f"Cannot normalize abscissa axis by {x2norm}")

        # we count the number of 1 in the shape of the data, which gives the real dimension of the data,
        # i.e. the number of reductions already performed (0 -> 3D, 1 -> 2D, 2 -> 1D)
        #        if self.shape.count(1) not in (1, 2):
        #            raise ValueError("data has to be 1D or 2D in order to call map.")
        dimension = len(wanted)

        if dimension == 1:
            meshgrid_conversion = self.coords._meshgrid_conversion()
            # abscissa = meshgrid_conversion[wanted[0]]
            abscissa_value = list(meshgrid_conversion.values())[0] / x1norm
            abscissa_key = list(meshgrid_conversion.keys())[0]

            datamoved_tmp = np.moveaxis(self.data, self.shape.index(1), 0)
            datamoved = np.moveaxis(
                datamoved_tmp[0], datamoved_tmp[0].shape.index(1), 0
            )
            dict_plotable = {
                "abscissa": abscissa_key,
                "field": data_key,
                abscissa_key: abscissa_value,
                data_key: datamoved[0],
            }
        if dimension == 2:
            # meshgrid in polar coordinates P, R (if "R", "phi") or R, P (if "phi", "R")
            # idem for all combinations of R,phi,z
            meshgrid_conversion = self.coords._meshgrid_conversion(*wanted)
            abscissa_value, ordinate_value = (
                meshgrid_conversion[wanted[0]] / x1norm,
                meshgrid_conversion[wanted[1]] / x2norm,
            )
            abscissa_key, ordinate_key = (wanted[0], wanted[1])
            # native_from_wanted = self.coords.native_from_wanted(*wanted)[0]

            ordered = meshgrid_conversion["ordered"]

            if ordered:
                data_value = self.data.T
                mfl_value = self.mfl.T
                # shape = np.shape(data_value)
                # if np.shape(abscissa_value) != shape:
                #     abscissa_value = abscissa_value[: shape[0], : shape[1]]
                # if np.shape(ordinate_value) != shape:
                #     ordinate_value = ordinate_value[: shape[0], : shape[1]]
            else:
                data_value = self.data
                mfl_value = self.mfl
                # shape = np.shape(data_value)
                # if np.shape(abscissa_value) != shape:
                #     abscissa_value = abscissa_value[: shape[0], : shape[1]]
                # if np.shape(ordinate_value) != shape:
                #     ordinate_value = ordinate_value[: shape[0], : shape[1]]

            dict_plotable = {
                "abscissa": abscissa_key,
                "ordinate": ordinate_key,
                "field2plot": data_key,
                abscissa_key: abscissa_value,
                ordinate_key: ordinate_value,
                data_key: data_value,
                "flux_func": mfl_value,
            }

        return Plotable(dict_plotable)


class GasDataSet:
    """
    Return:
        Dataset of the wanted quantities
    """

    def __init__(
        self,
        it: int,
        *,
        geometry: str = "unknown",
        directory: str = "",
        wanted_keys: str = "",
        spec: str = "electrons",
    ):
        self.it = it
        self.wanted_keys = wanted_keys
        self.spec = spec
        self.geometry = geometry
        self.directory = Path(directory)
        self.params = Parameters(directory=self.directory)
        self.simu_params = self.params.loadSimuParams()
        self.grid = Coordinates(self.directory, self.geometry)
        self._read = self.params.loadSimuFile(
            it=self.it, w_keys=self.wanted_keys, spec=self.spec
        )
        self.mfl = self._read["flux_func"]
        del self._read["flux_func"]
        self.dict = self._read
        for key in self.dict:
            self.dict[key] = GasField(
                key,
                self.dict[key],
                self.geometry,
                self.it,
                self.mfl,
                "",
                directory=directory,
            )

    def __getitem__(self, key):
        if key in self.dict:
            return self.dict[key]
        else:
            raise KeyError

    def keys(self):
        """
        Returns
        =======
        keys of the dict
        """
        return self.dict.keys()

    def values(self):
        """
        Returns
        =======
        values of the dict
        """
        return self.dict.values()

    def items(self):
        """
        Returns
        =======
        items of the dict
        """
        return self.dict.items()

    def update(self, var):
        """
        Args:
            var: dictionary to add to the existing one

        Returns:
            updated dictionary
        """

        for key, value in var.items():
            if key not in self.simu_params.keys():
                if key not in self.dict.keys():
                    self.dict[key] = GasField(
                        key,
                        value.data,
                        self.geometry,
                        self.it,
                        self.mfl,
                        "",
                        directory=self.directory,
                    )
                else:
                    self.dict[var.file + "_" + key] = GasField(
                        var.file + "_" + key,
                        value.data,
                        self.geometry,
                        self.it,
                        self.mfl,
                        "",
                        directory=self.directory,
                    )

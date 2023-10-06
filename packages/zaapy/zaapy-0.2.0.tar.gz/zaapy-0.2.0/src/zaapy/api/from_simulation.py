import glob
import re
from pathlib import Path
import numpy as np
import h5py

param_files = ["input_params.dat", "phys_params.dat"]


class Parameters:
    """
    Class to load input and physical parameters
    as well as data from Zeltron simulations.

    Args:
        directory: path towards simulation data
    """

    def __init__(self, directory):
        self.directory = Path(directory).joinpath("data")
        self.dict = {}

    def loadSimuParams(self):
        """
        Loads input and physical parameters of the simulation

        Returns:
            params: Dictionary of the parameters
        """

        params = {}
        for file in param_files:
            if not Path(self.directory).joinpath(file).is_file():
                raise FileNotFoundError(
                    f"{Path(self.directory).joinpath(file)} not found"
                )

        for name in param_files:
            file = open(Path(self.directory).joinpath(name))
            tmp = file.read().splitlines()  # list of lines
            # read the first line of tmp and grabs all the variable names by removing whitespaces
            keys = re.split("\s{2,}", tmp[0].strip())
            for i, k in enumerate(keys):
                params[k] = float(tmp[1].split()[i])
        if "BH spin" in params.keys():
            params["GR"] = True
        else:
            params["GR"] = False
        return params  # self.dict

    def loadSimuFile(self, it: int, w_keys: str, spec: str):
        """
        Loads any data

        Args:
            it: timestep to load
            folder: name of the folder where the data to load are
            file: exact name of the file to be loaded (do not write the timestep)
            keys: elements to load from this file

        Returns:
            dict: Dictionary of data loaded

        """
        count = 0
        if str(w_keys).find(",") != -1:
            w_keys = w_keys.split(",")
        else:
            w_keys = [w_keys]
        if Path(self.directory).joinpath(f"fields/fields_{it}.h5").is_file():
            tmp1 = h5py.File(
                Path(self.directory).joinpath(f"fields/fields_{it}.h5"), "r"
            )
            field_keys = list(tmp1.keys())
            count += 1
        else:
            field_keys = "No data loaded"

        if Path(self.directory).joinpath(f"densities/densities_{it}.h5").is_file():
            tmp2 = h5py.File(
                Path(self.directory).joinpath(f"densities/densities_{it}.h5"), "r"
            )
            dens_keys = list(tmp2.keys())
            count += 1
        else:
            dens_keys = "No data loaded"

        params = self.loadSimuParams()

        specJ = ""

        if not params["GR"]:
            specJ = f"_{spec}"

        if Path(self.directory).joinpath(f"currents/currents{specJ}_{it}.h5").is_file():
            tmp3 = h5py.File(
                Path(self.directory).joinpath(f"currents/currents{specJ}_{it}.h5"), "r"
            )
            currents_keys = list(tmp3.keys())
            count += 1
        else:
            currents_keys = "No data loaded"

        if spec.find("_") == -1:
            spec = f"_{spec}"
        # If data to load belongs to Tmunu file, the species is mandatory
        if Path(self.directory).joinpath(f"densities/Tmunu{spec}_{it}.h5").is_file():
            tmp4 = h5py.File(
                Path(self.directory).joinpath(f"densities/Tmunu{spec}_{it}.h5"), "r"
            )
            Tmunu_keys = list(tmp4.keys())
            count += 1
        else:
            Tmunu_keys = "No data loaded"

        if count == 0:
            raise ValueError(
                f"No data were found for timestep: \x1b[1;31m{it}\x1b[0m. (Frequency of DUMP = {params['FDUMP']})"
            )

        avail_keys = (
            list(field_keys) + list(dens_keys) + list(currents_keys) + list(Tmunu_keys)
        )

        for k in w_keys:
            if k not in avail_keys:
                raise ValueError(
                    f"{k} to plot in not a valid key for: \n fields: {field_keys},\n densities: {dens_keys},\n currents: {currents_keys},\n Tmunu: {Tmunu_keys}"
                )
            else:
                if k in field_keys:
                    self.dict[f"{k}"] = np.asarray(tmp1.get(k))
                elif k in dens_keys:
                    self.dict[f"{k}"] = np.asarray(tmp2.get(k))
                elif k in currents_keys:
                    self.dict[f"{k}"] = np.asarray(tmp3.get(k))
                elif k in Tmunu_keys:
                    self.dict[f"{k}"] = np.asarray(tmp4.get(k))
        if "Aphd" in field_keys:
            self.dict["flux_func"] = np.asarray(tmp1.get("Aphd"))
        elif "psi" in field_keys:
            self.dict["flux_func"] = np.asarray(tmp1.get("psi"))
        else:
            self.dict["flux_func"] = self.dict[list(self.dict.keys())[0]] * 0.0
        return self.dict

    def countSimuFiles(self):
        where = self.directory.joinpath("fields")
        self.data_files = [
            fn for fn in glob.glob1(where, "*.h5") if re.match(r"fields_\d+.h5", fn)
        ]

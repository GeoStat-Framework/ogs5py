# -*- coding: utf-8 -*-
"""Class for the ogs INITIAL_CONDITION file."""
import os
import numpy as np
import pandas as pd
from ogs5py.fileclasses.base import BlockFile, File
from ogs5py.tools.types import STRTYPE

CWD = os.getcwd()


class IC(BlockFile):
    """
    Class for the ogs INITIAL_CONDITION file.

    Parameters
    ----------
    task_root : str, optional
        Path to the destiny model folder.
        Default: cwd+"ogs5model"
    task_id : str, optional
        Name for the ogs task.
        Default: "model"

    Notes
    -----
    Main-Keywords (#):
        - INITIAL_CONDITION

    Sub-Keywords ($) per Main-Keyword:
        - INITIAL_CONDITION

            - PCS_TYPE
            - PRIMARY_VARIABLE
            - COMP_NAME
            - STORE_VALUES
            - DIS_TYPE
            - GEO_TYPE

    Standard block:
        :PCS_TYPE: "GROUNDWATER_FLOW"
        :PRIMARY_VARIABLE: "HEAD"
        :GEO_TYPE: "DOMAIN"
        :DIS_TYPE: ["CONSTANT", 0.0]

    Keyword documentation:
        https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/ic

    Reading routines:
        https://github.com/ufz/ogs5/blob/master/FEM/rf_ic_new.cpp#L222

    See Also
    --------
    add_block
    """

    MKEYS = ["INITIAL_CONDITION"]
    # sorted
    SKEYS = [
        [
            "PCS_TYPE",
            "PRIMARY_VARIABLE",
            "COMP_NAME",
            "STORE_VALUES",
            "DIS_TYPE",
            "GEO_TYPE",
        ]
    ]

    STD = {
        "PCS_TYPE": "GROUNDWATER_FLOW",
        "PRIMARY_VARIABLE": "HEAD",
        "GEO_TYPE": "DOMAIN",
        "DIS_TYPE": ["CONSTANT", 0.0],
    }

    def __init__(self, **OGS_Config):
        super(IC, self).__init__(**OGS_Config)
        self.file_ext = ".ic"


class RFR(File):
    """
    Class for the ogs RESTART file, if the DIS_TYPE in IC is set to RESTART.

    Parameters
    ----------
    variables : :class:`list` of :class:`str`, optional
        List of variable names.
        Default: :class:`None`
    data : :any:`numpy.ndarray`, optional
        RFR data. 2D array,
        where the first dimension is the number of variables.
        Default: :class:`None`
    units: :class:`list` of :class:`str`, optional
        List of units for the occurring variables. Can be None.
        OGS5 ignores them anyway.
        Default: :class:`None`
    headers : str or None, optional
        First four lines of the RFR file. If :class:`None`, a standard header
        is written.
        Default: :class:`None`
    name : str, optional
        File name for the RFR file. If :class:`None`, the task_id is used.
        Default: :class:`None`
    file_ext : :class:`str`, optional
        extension of the file (with leading dot ".rfr")
        Default: ".rfr"
    task_root : str, optional
        Path to the destiny model folder.
        Default: cwd+"ogs5model"
    task_id : str, optional
        Name for the ogs task.
        Default: "model"

    Notes
    -----
    First line (ignored):
        - #0#0#0#1#100000#0... (don't ask why)

    Second line (ignored):
        - 1 1 4 (don't ask why)

    Third line (information about Variables):
        - (No. of Var.) (No of data of 1. Var) (No of data of 2. Var) ...
        - 1 1 (example: 1 Variable with 1 component)
        - 2 1 1 (example: 2 Variables with 1 component each)
        - only 1 scalar per Variable allowed (bug in OGS5).
          See: https://github.com/ufz/ogs5/issues/151

    Fourth  line (Variable names and units):
        - (Name1), (Unit1), (Name2), (Unit2), ...
        - units are ignored

    Data (multiple lines):
        - (index) (Var1data1) .. (Var1dataN1) (Var2data1) .. (Var2dataN2) ...

    Keyword documentation:
        https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/ic

    Reading routines:
        https://github.com/ufz/ogs5/blob/master/FEM/rf_ic_new.cpp#L932
    """

    def __init__(
        self,
        variables=None,
        data=None,
        units=None,
        headers=None,
        name=None,
        file_ext=".rfr",
        task_root=None,
        task_id="model",
    ):
        super(RFR, self).__init__(task_root, task_id, file_ext)

        self.name = name
        if headers is None:  # Default 2 header lines (ignored by OGS5)
            headers = ["#0#0#0#1#100000#0#4.2.13 " + 41 * "#", "1 1 4"]
        self.headers = headers
        # content
        self._variables = None
        self._units = None
        self._data = None
        self.variables = variables
        self.units = units
        self.data = data

    @property
    def is_empty(self):
        """State if the OGS file is empty."""
        return not ((bool(self.variables)) and self.data.shape[1] > 0)

    @property
    def variables(self):
        """List of variables in the RFR file."""
        return self._variables

    @variables.setter
    def variables(self, var):
        if var is None:
            self._variables = []
        else:
            # strings could be detected as iterable, so check this first
            if isinstance(var, STRTYPE):
                var = [var]
            # convert iterators (like zip)
            try:
                iter(var)
            except TypeError:
                var = [str(var)]
            else:
                var = list(map(str, var))
            self._variables = var
        self.units = None
        self.data = None

    @property
    def units(self):
        """List of variable-units in the RFR file."""
        return self._units

    @units.setter
    def units(self, units):
        if not self.variables:  # no units without variables
            units = []
        # strings could be detected as iterable, so check this first
        if isinstance(units, STRTYPE):
            units = [units]
        # convert iterators (like zip)
        try:
            iter(units)
        except TypeError:
            units = [str(units)]
        else:
            units = list(map(str, units))
        if len(units) > len(self.variables):
            raise ValueError("RFR: More units than variables given.")
        if 1 < len(units) < len(self.variables):
            raise ValueError("RFR: Too few units given.")
        # if only 1 unit, use it for all variables
        if 1 == len(units) <= len(self.variables):
            units *= len(self.variables)
        self._units = units

    @property
    def data(self):
        """Data in the RFR file."""
        return self._data

    @data.setter
    def data(self, data):
        if data is None:
            data = np.empty((len(self.variables), 0), dtype=float)
        else:
            data = np.array(data, ndmin=2, dtype=float)
        if data.shape[0] != len(self.variables):
            raise ValueError("RFR: Number of data not in line with variables.")
        self._data = data

    @property
    def var_count(self):
        """Count of variables in the RFR file (line 3)."""
        return str(len(self.variables)) + " 1" * len(self.variables)

    @property
    def var_info(self):
        """Infos about variables and units in the RFR file (line 4)."""
        return " ".join(
            [
                var + ", " + unit
                for var, unit in zip(self.variables, self.units)
            ]
        )

    def check(self, verbose=True):
        """
        Check if the external geometry definition is valid.

        In the sence, that the contained data is consistent.

        Parameters
        ----------
        verbose : bool, optional
            Print information for the executed checks. Default: True

        Returns
        -------
        result : bool
            Validity of the given gli.
        """
        if self:
            if (
                len(self.variables) == len(self.units) == self.data.shape[0]
            ) and len(self.data.shape) == 2:
                if verbose:
                    print("RFR: valid.")
                return True
            if verbose:
                print("RFR: not valid.")
            return False
        return True

    def save(self, path, **kwargs):
        """
        Save the actual RFR external file in the given path.

        Parameters
        ----------
        path : str
            path to where to file should be saved
        """
        if self:
            with open(path, "w") as fout:
                for line in self.headers:
                    print(line, file=fout)
                print(self.var_count, file=fout)
                print(self.var_info, file=fout)
                data = pd.DataFrame(
                    index=np.arange(self.data.shape[1]),
                    columns=np.arange(len(self.variables) + 1),
                )
                data.loc[:, 0] = np.arange(self.data.shape[1])
                data.loc[:, 1:] = self.data.T
                data.to_csv(fout, header=None, index=None, sep=" ", mode="a")

    def read_file(self, path, encoding=None, verbose=False):
        """Write the actual RFR input file to the given folder."""
        # in python3 open was replaced with io.open
        from io import open

        headers = []
        variables = []
        units = []
        with open(path, "r", encoding=encoding) as fin:
            headers.append(fin.readline().splitlines()[0])  # 1. header line
            headers.append(fin.readline().splitlines()[0])  # 2. header line
            var_no = int(fin.readline().split()[0])
            var_info = fin.readline().split()
            for __ in range(var_no):
                var = var_info.pop(0)
                var = var[:-1] if var.endswith(",") else var
                unit = var_info.pop(0)
                variables.append(var)
                units.append(unit)
        if verbose:
            print("RFR.read_file: reading was fine.")
        self.headers = headers
        self.variables = variables
        self.units = units
        self.data = np.loadtxt(path, dtype=float, skiprows=4)[:, 1:].T
        if verbose:
            print("RFR.read_file: data conversion was fine.")

    def __repr__(self):
        """Representation."""
        out = ""
        for line in self.headers:
            out += line + "\n"
        out += self.var_count + "\n"
        out += self.var_info + "\n"
        for data_i, data_e in enumerate(self.data[:, :10].T):
            out += str(data_i) + " " + " ".join(map(str, data_e)) + "\n"
        if self.data.shape[1] > 10:
            out += "..."
        return out

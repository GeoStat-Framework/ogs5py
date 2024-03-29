# -*- coding: utf-8 -*-
"""Class for the ogs PHREEQC interface file."""
from ogs5py.fileclasses.base import LineFile


class PQC(LineFile):
    """
    Class for the ogs PHREEQC interface file.

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
    This is just handled as a line-wise file. You can access the data by line
    with:

        PQC.lines

    Keyword documentation:
        https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/pqc

    Reading routines:
        https://github.com/ufz/ogs5/blob/master/FEM/rf_react.cpp#L2136
    """

    def __init__(self, **OGS_Config):
        super().__init__(**OGS_Config)
        self.file_ext = ".pqc"


class PQCdat(LineFile):
    """
    Class for the ogs PHREEQC dat file.

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
    This is just handled as a line-wise file. You can access the data by line
    with:

        PQCdat.lines

    Keyword documentation:
        https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/pqc

    Reading routines:
        https://github.com/ufz/ogs5/blob/master/FEM/rf_react.cpp#L2136
    """

    def __init__(self, **OGS_Config):
        super().__init__(**OGS_Config)
        self.name = "phreeqc"
        self.file_ext = ".dat"

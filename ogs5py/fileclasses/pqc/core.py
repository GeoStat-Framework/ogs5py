"""
Class for the ogs PHREEQC interface file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import LineFile


class PQC(LineFile):
    """
    Class for the ogs PHREEQC interface file.

    Info
    ----
    This is just handled as a line-wise file. You can access the data by line
    with:
        PQC.lines

    https://svn.ufz.de/ogs/wiki/public/doc-auto/by_ext/pqc

    https://github.com/ufz/ogs5/blob/master/FEM/rf_react.cpp#L2136
    """

    def __init__(self, **OGS_Config):
        """
        Input
        -----

        OGS_Config dictonary

        """
        super(PQC, self).__init__(**OGS_Config)
        self.file_ext = ".pqc"

    @property
    def file_name(self):
        return self.task_id

    @file_name.setter
    def file_name(self, value):
        self.task_id = value


class PQCdat(LineFile):
    """
    Class for the ogs PHREEQC dat file.

    Info
    ----
    This is just handled as a line-wise file. You can access the data by line
    with:
        PQCdat.lines

    https://svn.ufz.de/ogs/wiki/public/doc-auto/by_ext/pqc

    https://github.com/ufz/ogs5/blob/master/FEM/rf_react.cpp#L2136
    """

    def __init__(self, **OGS_Config):
        """
        Input
        -----

        OGS_Config dictonary

        """
        super(PQCdat, self).__init__(**OGS_Config)
        self.file_name = "phreeqc"
        self.file_ext = ".dat"

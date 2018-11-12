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
        self.file_name = self.task_id
        self.file_ext = ".pqc"

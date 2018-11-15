"""
Class for the ogs ASC file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import LineFile


class ASC(LineFile):
    """
    Class for the ogs ASC file.

    Info
    ----
    This is just handled as a line-wise file. You can access the data by line
    with:
        ASC.lines

    This file type comes either from .tim .pcs or .gem
    """

    def __init__(self, **OGS_Config):
        """
        Input
        -----

        OGS_Config dictonary

        """
        super(ASC, self).__init__(**OGS_Config)
        self.file_ext = ".asc"

"""
Class for the ogs USER DEFINED TIME CURVES file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import OGSfile


class RFD(OGSfile):
    """
    Class for the ogs USER DEFINED TIME CURVES file.

    Keywords for a block
    --------------------
    - PROJECT
    - CURVE
    - CURVES

    Standard block
    --------------
    None

    Info
    ----
    See: ``add_block``

    https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/rfd

    https://github.com/ufz/ogs5/blob/master/FEM/files0.cpp#L370
    """

    MKEYS = ["PROJECT", "CURVE", "CURVES"]
    # just a workaround in this case... since all content is related to mainkw
    SKEYS = [[""], [""], [""]]

    STD = {}

    def __init__(self, **OGS_Config):
        """
        Input
        -----

        OGS_Config dictonary

        """
        super(RFD, self).__init__(**OGS_Config)
        self.file_ext = ".rfd"

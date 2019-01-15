"""
Class for the ogs FUNCTION file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import BlockFile


class FCT(BlockFile):
    """
    Class for the ogs FUNCTION file.

    Keywords for a block
    --------------------
    - FUNCTION
        - DATA
        - DIMENSION
        - DIS_TYPE
        - GEO_TYPE
        - MATRIX
        - TYPE
        - VARIABLES

    Standard block
    --------------
    None

    Info
    ----
    See: ``add_block``

    https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/fct

    https://github.com/ufz/ogs5/blob/master/FEM/rf_fct.cpp#L82
    """

    MKEYS = ["FUNCTION"]
    # sorted
    SKEYS = [
        [
            "TYPE",
            "GEO_TYPE",
            "DIS_TYPE",
            "VARIABLES",
            "DIMENSION",
            "MATRIX",
            "DATA",
        ]
    ]

    STD = {}

    def __init__(self, **OGS_Config):
        """
        Input
        -----

        OGS_Config dictonary

        """
        super(FCT, self).__init__(**OGS_Config)
        self.file_ext = ".fct"

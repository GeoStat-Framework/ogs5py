# -*- coding: utf-8 -*-
"""
Class for the ogs FUNCTION file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import BlockFile


class FCT(BlockFile):
    """
    Class for the ogs FUNCTION file.

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
        - FUNCTION

    Sub-Keywords ($) per Main-Keyword:
        - FUNCTION

            - DATA
            - DIMENSION
            - DIS_TYPE
            - GEO_TYPE
            - MATRIX
            - TYPE
            - VARIABLES

    Standard block:
        None

    Keyword documentation:
        https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/fct

    Reading routines:
        https://github.com/ufz/ogs5/blob/master/FEM/rf_fct.cpp#L82

    See Also
    --------
    add_block
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
        super(FCT, self).__init__(**OGS_Config)
        self.file_ext = ".fct"

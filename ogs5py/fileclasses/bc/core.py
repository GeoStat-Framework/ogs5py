"""
Class for the ogs BOUNDARY CONDITION file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import BlockFile


class BC(BlockFile):
    """
    Class for the ogs BOUNDARY CONDITION file.

    Notes
    -----
    Main-Keywords (#) :
        - BOUNDARY_CONDITION

    Sub-Keywords ($) per Main-Keyword:
        - BOUNDARY_CONDITION

            - COMP_NAME
            - CONSTRAINED
            - COPY_VALUE
            - DIS_TYPE
            - DIS_TYPE_CONDITION
            - EPSILON
            - EXCAVATION
            - FCT_TYPE
            - GEO_TYPE
            - MSH_TYPE
            - NO_DISP_INCREMENT
            - PCS_TYPE
            - PRESSURE_AS_HEAD
            - PRIMARY_VARIABLE
            - TIME_CONTROLLED_ACTIVE
            - TIM_TYPE

    Standard block
    --------------
    :PCS_TYPE: "GROUNDWATER_FLOW"
    :PRIMARY_VARIABLE: "HEAD"
    :DIS_TYPE: ["CONSTANT", 0.0]
    :GEO_TYPE: ["POLYLINE", "boundary"]

    Info
    ----
    See: ``add_block``

    https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/bc

    https://github.com/ufz/ogs5/blob/master/FEM/rf_bc_new.cpp#L228
    """

    MKEYS = ["BOUNDARY_CONDITION"]
    SKEYS = [
        [
            "PCS_TYPE",
            "PRIMARY_VARIABLE",
            "COMP_NAME",
            "GEO_TYPE",
            "DIS_TYPE",
            "TIM_TYPE",
            "FCT_TYPE",
            "MSH_TYPE",
            "DIS_TYPE_CONDITION",
            "EPSILON",
            "TIME_CONTROLLED_ACTIVE",
            "EXCAVATION",
            "NO_DISP_INCREMENT",
            "COPY_VALUE",
            "PRESSURE_AS_HEAD",
            "CONSTRAINED",
        ]
    ]

    STD = {
        "PCS_TYPE": "GROUNDWATER_FLOW",
        "PRIMARY_VARIABLE": "HEAD",
        "DIS_TYPE": ["CONSTANT", 0.0],
        "GEO_TYPE": ["POLYLINE", "boundary"],
    }

    def __init__(self, **OGS_Config):
        """
        Input
        -----

        OGS_Config dictonary

        """
        super(BC, self).__init__(**OGS_Config)
        self.file_ext = ".bc"
        self.force_writing = True

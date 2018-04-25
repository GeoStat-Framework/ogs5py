"""
Class for the ogs BOUNDARY CONDITION file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import OGSfile


class BC(OGSfile):
    """
    Class for the ogs BOUNDARY CONDITION file.

    Keywords for a block
    --------------------
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
    :DIS_TYPE: [["CONSTANT", 0.0]]
    :GEO_TYPE: [["POLYLINE", "BC"]]

    Info
    ----
    See: ``add_block``
    """

    MKEYS = ["BOUNDARY_CONDITION"]
    SKEYS = [["COMP_NAME",
              "CONSTRAINED",
              "COPY_VALUE",
              "DIS_TYPE",
              "DIS_TYPE_CONDITION",
              "EPSILON",
              "EXCAVATION",
              "FCT_TYPE",
              "GEO_TYPE",
              "MSH_TYPE",
              "NO_DISP_INCREMENT",
              "PCS_TYPE",
              "PRESSURE_AS_HEAD",
              "PRIMARY_VARIABLE",
              "TIME_CONTROLLED_ACTIVE",
              "TIM_TYPE"]]

    STD = {"PCS_TYPE": "GROUNDWATER_FLOW",
           "PRIMARY_VARIABLE": "HEAD",
           "DIS_TYPE": [["CONSTANT", 0.0]],
           "GEO_TYPE": [["POLYLINE", "BC"]]}

    def __init__(self, **OGS_Config):
        '''
        Input
        -----

        OGS_Config dictonary

        '''
        super(BC, self).__init__(**OGS_Config)
        self.f_type = '.bc'

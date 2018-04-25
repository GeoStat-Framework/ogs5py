'''
Class for the ogs SOURCE_TERM file.
'''

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import OGSfile


class ST(OGSfile):
    """
    Class for the ogs SOURCE_TERM file.

    Keywords for a block
    --------------------
    - SOURCE_TERM
        - AIR_BREAKING
        - CHANNEL
        - COMP_NAME
        - CONSTRAINED
        - DISTRIBUTE_VOLUME_FLUX
        - DIS_TYPE
        - EXPLICIT_SURFACE_WATER_PRESSURE
        - FCT_TYPE
        - GEO_TYPE
        - MSH_TYPE
        - NEGLECT_SURFACE_WATER_PRESSURE
        - NODE_AVERAGING
        - PCS_TYPE
        - PRIMARY_VARIABLE
        - TIME_INTERPOLATION
        - TIM_TYPE

    Standard block
    --------------
    :PCS_TYPE: "GROUNDWATER_FLOW"
    :PRIMARY_VARIABLE: "HEAD"
    :GEO_TYPE: [["POINT", "WELL"]]
    :DIS_TYPE: [["CONSTANT_NEUMANN", -1.0e-03]]

    Info
    ----
    See: ``add_block``
    """

    MKEYS = ["SOURCE_TERM"]
    SKEYS = [["AIR_BREAKING",
              "CHANNEL",
              "COMP_NAME",
              "CONSTRAINED",
              "DISTRIBUTE_VOLUME_FLUX",
              "DIS_TYPE",
              "EXPLICIT_SURFACE_WATER_PRESSURE",
              "FCT_TYPE",
              "GEO_TYPE",
              "MSH_TYPE",
              "NEGLECT_SURFACE_WATER_PRESSURE",
              "NODE_AVERAGING",
              "PCS_TYPE",
              "PRIMARY_VARIABLE",
              "TIME_INTERPOLATION",
              "TIM_TYPE"]]

    STD = {"PCS_TYPE": "GROUNDWATER_FLOW",
           "PRIMARY_VARIABLE": "HEAD",
           "GEO_TYPE": [["POINT", "WELL"]],
           "DIS_TYPE": [["CONSTANT_NEUMANN", -1.0e-03]]}

    def __init__(self, **OGS_Config):
        '''
        Input
        -----

        OGS_Config dictonary

        '''
        super(ST, self).__init__(**OGS_Config)
        self.f_type = '.st'

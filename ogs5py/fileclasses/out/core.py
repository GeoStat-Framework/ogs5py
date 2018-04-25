'''
Class for the ogs OUTPUT file.
'''

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import OGSfile


class OUT(OGSfile):
    """
    Class for the ogs OUTPUT file.

    Keywords for a block
    --------------------
    - OUTPUT
        - AMPLIFIER
        - DAT_TYPE
        - DIS_TYPE
        - ELE_VALUES
        - GEO_TYPE
        - MFP_VALUES
        - MMP_VALUES
        - MSH_TYPE
        - NOD_VALUES
        - PCON_VALUES
        - PCS_TYPE
        - RWPT_VALUES
        - TECPLOT_ZONE_SHARE
        - TIM_TYPE
        - VARIABLESHARING

    Standard block
    --------------
    :NOD_VALUES: "HEAD"
    :GEO_TYPE: "DOMAIN"
    :DAT_TYPE: "PVD"
    :TIM_TYPE: [["STEPS", 1]]

    Info
    ----
    See: ``add_block``
    """

    MKEYS = ["OUTPUT"]
    SKEYS = [["AMPLIFIER",
              "DAT_TYPE",
              "DIS_TYPE",
              "ELE_VALUES",
              "GEO_TYPE",
              "MFP_VALUES",
              "MMP_VALUES",
              "MSH_TYPE",
              "NOD_VALUES",
              "PCON_VALUES",
              "PCS_TYPE",
              "RWPT_VALUES",
              "TECPLOT_ZONE_SHARE",
              "TIM_TYPE",
              "VARIABLESHARING"]]

    STD = {"NOD_VALUES": "HEAD",
           "GEO_TYPE": "DOMAIN",
           "DAT_TYPE": "PVD",
           "TIM_TYPE": [["STEPS", 1]]}

    def __init__(self, **OGS_Config):
        '''
        Input
        -----

        OGS_Config dictonary

        '''
        super(OUT, self).__init__(**OGS_Config)
        self.f_type = '.out'

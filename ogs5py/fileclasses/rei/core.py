'''
Class for the ogs REACTION_INTERFACE file.
'''

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import OGSfile


class REI(OGSfile):
    """
    Class for the ogs REACTION_INTERFACE file.

    Keywords for a block
    --------------------
    - REACTION_INTERFACE
        - ALL_PCS_DUMP
        - DISSOLVED_NEUTRAL_CO2_SPECIES_NAME
        - HEATPUMP_2DH_TO_2DV
        - INITIAL_CONDITION_OUTPUT
        - MOL_PER
        - PCS_RENAME_INIT
        - PCS_RENAME_POST
        - PCS_RENAME_PRE
        - POROSITY_RESTART
        - PRESSURE
        - P_VLE
        - RESIDUAL
        - SODIUM_SPECIES_NAME
        - SOLID_SPECIES_DUMP_MOLES
        - TEMPERATURE
        - UPDATE_INITIAL_SOLID_COMPOSITION
        - VLE
        - WATER_CONCENTRATION
        - WATER_SATURATION_LIMIT
        - WATER_SPECIES_NAME

    Standard block
    --------------
    None

    Info
    ----
    See: ``add_block``
    """

    MKEYS = ["REACTION_INTERFACE"]
    SKEYS = [["ALL_PCS_DUMP",
              "DISSOLVED_NEUTRAL_CO2_SPECIES_NAME",
              "HEATPUMP_2DH_TO_2DV",
              "INITIAL_CONDITION_OUTPUT",
              "MOL_PER",
              "PCS_RENAME_INIT",
              "PCS_RENAME_POST",
              "PCS_RENAME_PRE",
              "POROSITY_RESTART",
              "PRESSURE",
              "P_VLE",
              "RESIDUAL",
              "SODIUM_SPECIES_NAME",
              "SOLID_SPECIES_DUMP_MOLES",
              "TEMPERATURE",
              "UPDATE_INITIAL_SOLID_COMPOSITION",
              "VLE",
              "WATER_CONCENTRATION",
              "WATER_SATURATION_LIMIT",
              "WATER_SPECIES_NAME"]]

    STD = {}

    def __init__(self, **OGS_Config):
        '''
        Input
        -----

        OGS_Config dictonary

        '''
        super(REI, self).__init__(**OGS_Config)
        self.f_type = '.rei'

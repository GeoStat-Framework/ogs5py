'''
Class for the ogs PROCESS file.
'''

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import OGSfile


class PCS(OGSfile):
    """
    Class for the ogs PROCESS file.

    Keywords for a block
    --------------------
    - PROCESS
        - APP_TYPE
        - BOUNDARY_CONDITION_OUTPUT
        - COUNT
        - CPL_TYPE
        - DEACTIVATED_SUBDOMAIN
        - DISSOLVED_CO2_INGAS_PCS_NAME
        - DISSOLVED_CO2_PCS_NAME
        - ELEMENT_MATRIX_OUTPUT
        - GEO_TYPE
        - MEDIUM_TYPE
        - MEMORY_TYPE
        - MSH_TYPE
        - NEGLECT_H_INI_EFFECT
        - NUM_TYPE
        - OutputMassOfGasInModel
        - PCS_TYPE
        - PHASE_TRANSITION
        - PRIMARY_VARIABLE
        - PROCESSED_BC
        - RELOAD
        - SATURATION_SWITCH
        - SAVE_ECLIPSE_DATA_FILES
        - SIMULATOR
        - SIMULATOR_MODEL_PATH
        - SIMULATOR_PATH
        - SIMULATOR_WELL_PATH
        - ST_RHS
        - TIME_CONTROLLED_EXCAVATION
        - TIM_TYPE
        - UPDATE_INI_STATE
        - USE_PRECALCULATED_FILES
        - USE_VELOCITIES_FOR_TRANSPORT

    Standard block
    --------------
    :PCS_TYPE: "GROUNDWATER_FLOW"
    :NUM_TYPE: "NEW"

    Info
    ----
    See: ``add_block``
    """

    MKEYS = ["PROCESS"]
    SKEYS = [["APP_TYPE",
              "BOUNDARY_CONDITION_OUTPUT",
              "COUNT",
              "CPL_TYPE",
              "DEACTIVATED_SUBDOMAIN",
              "DISSOLVED_CO2_INGAS_PCS_NAME",
              "DISSOLVED_CO2_PCS_NAME",
              "ELEMENT_MATRIX_OUTPUT",
              "GEO_TYPE",
              "MEDIUM_TYPE",
              "MEMORY_TYPE",
              "MSH_TYPE",
              "NEGLECT_H_INI_EFFECT",
              "NUM_TYPE",
              "OutputMassOfGasInModel",
              "PCS_TYPE",
              "PHASE_TRANSITION",
              "PRIMARY_VARIABLE",
              "PROCESSED_BC",
              "RELOAD",
              "SATURATION_SWITCH",
              "SAVE_ECLIPSE_DATA_FILES",
              "SIMULATOR",
              "SIMULATOR_MODEL_PATH",
              "SIMULATOR_PATH",
              "SIMULATOR_WELL_PATH",
              "ST_RHS",
              "TIME_CONTROLLED_EXCAVATION",
              "TIM_TYPE",
              "UPDATE_INI_STATE",
              "USE_PRECALCULATED_FILES",
              "USE_VELOCITIES_FOR_TRANSPORT"]]

    STD = {"PCS_TYPE": "GROUNDWATER_FLOW",
           "NUM_TYPE": "NEW"}

    def __init__(self, **OGS_Config):
        '''
        Input
        -----

        OGS_Config dictonary

        '''
        super(PCS, self).__init__(**OGS_Config)
        self.f_type = '.pcs'

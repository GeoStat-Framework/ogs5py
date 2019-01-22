# -*- coding: utf-8 -*-
"""
Class for the ogs PROCESS file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import BlockFile


class PCS(BlockFile):
    """
    Class for the ogs PROCESS file.

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
        - PROCESS

    Sub-Keywords ($) per Main-Keyword:
        - PROCESS

            - APP_TYPE
            - BOUNDARY_CONDITION_OUTPUT
            - COUNT
            - CPL_TYPE
            - DEACTIVATED_SUBDOMAIN
            - DISSOLVED_CO2_INGAS_PCS_NAME
            - DISSOLVED_CO2_PCS_NAME
            - TEMPERATURE_UNIT
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

    Standard block:
        :PCS_TYPE: "GROUNDWATER_FLOW"
        :NUM_TYPE: "NEW"

    Keyword documentation:
        https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/pcs

    Reading routines:
        https://github.com/ufz/ogs5/blob/master/FEM/rf_pcs.cpp#L1803

    See Also
    --------
    add_block
    """

    MKEYS = ["PROCESS"]
    # sorted
    SKEYS = [
        [
            "PCS_TYPE",
            "NUM_TYPE",
            "CPL_TYPE",
            "TIM_TYPE",
            "APP_TYPE",
            "COUNT",
            "PRIMARY_VARIABLE",
            "TEMPERATURE_UNIT",
            "ELEMENT_MATRIX_OUTPUT",
            "BOUNDARY_CONDITION_OUTPUT",
            "OutputMassOfGasInModel",
            "ST_RHS",
            "PROCESSED_BC",
            "MEMORY_TYPE",
            "RELOAD",
            "DEACTIVATED_SUBDOMAIN",
            "MSH_TYPE",
            #        "GEO_TYPE",
            "MEDIUM_TYPE",
            "SATURATION_SWITCH",
            "USE_VELOCITIES_FOR_TRANSPORT",
            "SIMULATOR",  # really?
            "SIMULATOR_PATH",
            "SIMULATOR_MODEL_PATH",
            "USE_PRECALCULATED_FILES",
            "SAVE_ECLIPSE_DATA_FILES",
            "SIMULATOR_WELL_PATH",
            "PHASE_TRANSITION",
            "DISSOLVED_CO2_PCS_NAME",
            "DISSOLVED_CO2_INGAS_PCS_NAME",
            "TIME_CONTROLLED_EXCAVATION",
            "NEGLECT_H_INI_EFFECT",
            "UPDATE_INI_STATE",
            "CONSTANT",
        ]
    ]

    STD = {"PCS_TYPE": "GROUNDWATER_FLOW", "NUM_TYPE": "NEW"}

    def __init__(self, **OGS_Config):
        super(PCS, self).__init__(**OGS_Config)
        self.file_ext = ".pcs"
        self.force_writing = True

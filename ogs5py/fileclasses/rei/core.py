# -*- coding: utf-8 -*-
"""
Class for the ogs REACTION_INTERFACE file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import BlockFile


class REI(BlockFile):
    """
    Class for the ogs REACTION_INTERFACE file.

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
        - REACTION_INTERFACE

    Sub-Keywords ($) per Main-Keyword:
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

    Standard block:
        None

    Keyword documentation:
        https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/rei

    Reading routines:
        https://github.com/ufz/ogs5/blob/master/FEM/rf_react_int.cpp#L173

    See Also
    --------
    add_block
    """

    MKEYS = ["REACTION_INTERFACE"]
    # sorted
    SKEYS = [
        [
            "MOL_PER",
            "WATER_CONCENTRATION",
            "WATER_SPECIES_NAME",
            "DISSOLVED_NEUTRAL_CO2_SPECIES_NAME",
            "SODIUM_SPECIES_NAME",
            "PRESSURE",
            "TEMPERATURE",
            "WATER_SATURATION_LIMIT",
            "RESIDUAL",
            "SOLID_SPECIES_DUMP_MOLES",
            "ALL_PCS_DUMP",
            "INITIAL_CONDITION_OUTPUT",
            "UPDATE_INITIAL_SOLID_COMPOSITION",
            "VLE",
            "P_VLE",
            "POROSITY_RESTART",
            "HEATPUMP_2DH_TO_2DV",
            "PCS_RENAME_INIT",
            "PCS_RENAME_PRE",
            "PCS_RENAME_POST",
            "CONSTANT_PRESSURE",  # really?
            "CONSTANT_TEMPERATURE",  # really?
        ]
    ]

    STD = {}

    def __init__(self, **OGS_Config):
        super(REI, self).__init__(**OGS_Config)
        self.file_ext = ".rei"

# -*- coding: utf-8 -*-
"""
Class for the ogs SOLID_PROPERTIES file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import BlockFile


class MSP(BlockFile):
    """
    Class for the ogs SOLID_PROPERTIES file.

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
        - SOLID_PROPERTIES

    Sub-Keywords ($) per Main-Keyword:
        - SOLID_PROPERTIES

            - BIOT_CONSTANT
            - CREEP
            - DENSITY
            - ELASTICITY
            - EXCAVATION
            - E_Function
            - GRAVITY_CONSTANT
            - MICRO_STRUCTURE_PLAS
            - NAME
            - NON_REACTIVE_FRACTION
            - PLASTICITY
            - REACTIVE_SYSTEM
            - SOLID_BULK_MODULUS
            - SPECIFIC_HEAT_SOURCE
            - STRESS_INTEGRATION_TOLERANCE
            - STRESS_UNIT
            - SWELLING_PRESSURE_TYPE
            - THERMAL
            - THRESHOLD_DEV_STR
            - TIME_DEPENDENT_YOUNGS_POISSON

    Standard block:
        None

    Keyword documentation:
        https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/msp

    Reading routines:
        https://github.com/ufz/ogs5/blob/master/FEM/rf_msp_new.cpp#L65

    See Also
    --------
    add_block
    """

    MKEYS = ["SOLID_PROPERTIES"]
    # sorted (some sub keys even have sub-sub keys)
    SKEYS = [
        [
            "NAME",
            "SWELLING_PRESSURE_TYPE",
            "DENSITY",
            "THERMAL",
            "ELASTICITY",
            "EXCAVATION",
            "E_Function",
            "TIME_DEPENDENT_YOUNGS_POISSON",
            "CREEP",
            "THRESHOLD_DEV_STR",
            "BIOT_CONSTANT",
            "SOLID_BULK_MODULUS",
            "STRESS_INTEGRATION_TOLERANCE",
            "STRESS_UNIT",
            "GRAVITY_CONSTANT",
            "GRAVITY_RAMP",
            "PLASTICITY",
            "REACTIVE_SYSTEM",
            "NON_REACTIVE_FRACTION",
            "SPECIFIC_HEAT_SOURCE",
            "ENTHALPY_CORRECTION_REFERENCE_TEMPERATURE",
            "MICRO_STRUCTURE_PLAS",
        ]
    ]

    STD = {}

    def __init__(self, **OGS_Config):
        super(MSP, self).__init__(**OGS_Config)
        self.file_ext = ".msp"

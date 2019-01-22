# -*- coding: utf-8 -*-
"""
Class for the ogs FLUID PROPERTY file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import BlockFile


class MFP(BlockFile):
    """
    Class for the ogs FLUID PROPERTY file.

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
        - FLUID_PROPERTIES

    Sub-Keywords ($) per Main-Keyword:
        - FLUID_PROPERTIES

            - COMPONENTS
            - COMPRESSIBILITY
            - DAT_TYPE
            - DECAY
            - DENSITY
            - DIFFUSION
            - DRHO_DT_UNSATURATED
            - EOS_TYPE
            - FLUID_NAME
            - FLUID_TYPE
            - GRAVITY
            - HEAT_CONDUCTIVITY
            - ISOTHERM
            - JTC
            - NON_GRAVITY
            - PHASE_DIFFUSION
            - SPECIFIC_HEAT_CAPACITY
            - SPECIFIC_HEAT_SOURCE
            - TEMPERATURE
            - VISCOSITY

    Standard block:
        :FLUID_TYPE: "LIQUID"
        :DENSITY: [1, 1.0e+03]
        :VISCOSITY: [1, 1.0e-03]

    Keyword documentation:
        https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/mfp

    Reading routines:
        https://github.com/ufz/ogs5/blob/master/FEM/rf_mfp_new.cpp#L140

    See Also
    --------
    add_block
    """

    MKEYS = ["FLUID_PROPERTIES"]
    # sorted
    SKEYS = [
        [
            "FLUID_TYPE",
            "COMPONENTS",
            "FLUID_NAME",
            "EOS_TYPE",
            "COMPRESSIBILITY",
            "JTC",
            "DAT_TYPE",
            "NON_GRAVITY",
            "DRHO_DT_UNSATURATED",
            "DENSITY",
            "TEMPERATURE",
            "VISCOSITY",
            "SPECIFIC_HEAT_CAPACITY",
            "SPECIFIC_HEAT_CONDUCTIVITY",  # really?
            "HEAT_CAPACITY",  # really?
            "HEAT_CONDUCTIVITY",
            "PHASE_DIFFUSION",
            "DIFFUSION",
            "DECAY",
            "ISOTHERM",
            "GRAVITY",
            "SPECIFIC_HEAT_SOURCE",
            "PCS_TYPE",  # really?
            "THERMAL",  # really?
        ]
    ]

    STD = {
        "FLUID_TYPE": "LIQUID",
        "DENSITY": [1, 1.0e03],
        "VISCOSITY": [1, 1.0e-03],
    }

    def __init__(self, **OGS_Config):
        super(MFP, self).__init__(**OGS_Config)
        self.file_ext = ".mfp"

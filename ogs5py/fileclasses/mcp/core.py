# -*- coding: utf-8 -*-
"""
Class for the ogs COMPONENT_PROPERTIES file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import BlockFile


class MCP(BlockFile):
    """
    Class for the ogs COMPONENT_PROPERTIES file.

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
        - COMPONENT_PROPERTIES

    Sub-Keywords ($) per Main-Keyword:
        - COMPONENT_PROPERTIES

            - ACENTRIC_FACTOR
            - A_ZERO
            - BUBBLE_VELOCITY
            - CRITICAL_PRESSURE
            - CRITICAL_TEMPERATURE
            - DECAY
            - DIFFUSION
            - FLUID_ID
            - FLUID_PHASE
            - FORMULA
            - ISOTHERM
            - MAXIMUM_AQUEOUS_SOLUBILITY
            - MINERAL_DENSITY
            - MOBILE
            - MOLAR_DENSITY
            - MOLAR_VOLUME
            - MOLAR_WEIGHT
            - MOL_MASS
            - NAME
            - OutputMassOfComponentInModel
            - TRANSPORT_PHASE
            - VALENCE
            - VOLUME_DIFFUSION

    Standard block:
        None

    Keyword documentation:
        https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/mcp

    Reading routines:
        https://github.com/ufz/ogs5/blob/master/FEM/rfmat_cp.cpp#L269

    See Also
    --------
    add_block
    """

    MKEYS = ["COMPONENT_PROPERTIES"]
    # sorted
    SKEYS = [
        [
            "NAME",
            "FORMULA",
            "MOBILE",
            "TRANSPORT_PHASE",
            "FLUID_PHASE",
            "MOL_MASS",
            "CRITICAL_PRESSURE",
            "CRITICAL_TEMPERATURE",
            "ACENTRIC_FACTOR",
            "FLUID_ID",
            "MOLAR_VOLUME",
            "VOLUME_DIFFUSION",
            "MINERAL_DENSITY",
            "DIFFUSION",
            "DECAY",
            "ISOTHERM",
            "BUBBLE_VELOCITY",
            "MOLAR_DENSITY",
            "MOLAR_WEIGHT",
            "MAXIMUM_AQUEOUS_SOLUBILITY",
            "OutputMassOfComponentInModel",
            "VALENCE",
            "A_ZERO",
            "CRITICAL_VOLUME",  # really?
            "CRITICAL_DENSITY",  # really?
            "COMP_CAPACITY",  # really?
            "COMP_CONDUCTIVITY",  # really?
            "SOLUTE",  # really?
            "MOLECULAR_WEIGHT",  # really?
        ]
    ]

    STD = {}

    def __init__(self, **OGS_Config):
        super(MCP, self).__init__(**OGS_Config)
        self.file_ext = ".mcp"

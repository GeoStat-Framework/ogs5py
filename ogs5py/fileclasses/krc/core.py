# -*- coding: utf-8 -*-
"""
Class for the ogs KINETRIC REACTION file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import BlockFile


class KRC(BlockFile):
    """
    Class for the ogs KINETRIC REACTION file.

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
        - MICROBE_PROPERTIES
        - KINREACTIONDATA
        - BLOB_PROPERTIES
        - REACTION

    Sub-Keywords ($) per Main-Keyword:
        - MICROBE_PROPERTIES

            - MICROBENAME
            - _drmc__PARAMETERS
            - MONOD_REACTION_NAME

        - REACTION

            - NAME
            - TYPE
            - BACTERIANAME
            - EQUATION
            - RATECONSTANT
            - GROWTH
            - MONODTERMS
            - THRESHHOLDTERMS
            - INHIBITIONTERMS
            - PRODUCTIONTERMS
            - PRODUCTIONSTOCH
            - BACTERIAL_YIELD
            - ISOTOPE_FRACTIONATION
            - BACTERIA_SPECIFIC_CAPACITY
            - TEMPERATURE_DEPENDENCE
            - _drmc_
            - STANDARD_GIBBS_ENERGY
            - EXCHANGE_PARAMETERS
            - SORPTION_TYPE
            - NAPL_PROPERTIES
            - REACTION_ORDER
            - MINERALNAME
            - CHEMAPPNAME
            - EQUILIBRIUM_CONSTANT
            - RATE_EXPONENTS
            - REACTIVE_SURFACE_AREA
            - PRECIPITATION_BY_BASETERM_ONLY
            - PRECIPITATION_FACTOR
            - PRECIPITATION_EXPONENT
            - BASETERM
            - MECHANISMTERM
            - SWITCH_OFF_GEOMETRY

        - BLOB_PROPERTIES

            - NAME
            - D50
            - DM
            - DS
            - UI
            - NAPL_CONTENT_INI
            - NAPL_CONTENT_RES
            - GRAIN_SPHERE_RATIO
            - TORTUOSITY
            - LENGTH
            - CALC_SHERWOOD
            - CALC_SHERWOOD_MODIFIED
            - SHERWOOD_MODEL
            - GEOMETRY
            - GAS_DISSOLUTION
            - INTERFACIAL_AREA

        - KINREACTIONDATA

            - SOLVER_TYPE
            - RELATIVE_ERROR
            - MIN_TIMESTEP
            - INITIAL_TIMESTEP
            - BACTERIACAPACITY
            - MIN_BACTERIACONC
            - MIN_CONCENTRATION_REPLACE
            - SURFACES
            - ALLOW_REACTIONS
            - NO_REACTIONS
            - COPY_CONCENTRATIONS
            - LAGNEAU_BENCHMARK
            - SCALE_DCDT
            - SORT_NODES
            - OMEGA_THRESHOLD
            - REACTION_DEACTIVATION
            - DEBUG_OUTPUT
            - ACTIVITY_MODEL

    Standard block:
        None

    Keyword documentation:
        https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/krc

    Reading routines:
        https://github.com/ufz/ogs5/blob/master/FEM/rf_kinreact.cpp

        MICROBE_PROPERTIES :
            https://github.com/ufz/ogs5/blob/master/FEM/rf_kinreact.cpp#L232
        REACTION :
            https://github.com/ufz/ogs5/blob/master/FEM/rf_kinreact.cpp#L1549
        BLOB_PROPERTIES :
            https://github.com/ufz/ogs5/blob/master/FEM/rf_kinreact.cpp#L2622
        KINREACTIONDATA :
            https://github.com/ufz/ogs5/blob/master/FEM/rf_kinreact.cpp#L3185

    See Also
    --------
    add_block
    """

    MKEYS = [
        "MICROBE_PROPERTIES",
        "REACTION",
        "BLOB_PROPERTIES",
        "KINREACTIONDATA",
    ]
    # these are not sorted at the moment
    SKEYS = [
        [  # MICROBE_PROPERTIES
            "MICROBENAME",
            "_drmc__PARAMETERS",
            "MONOD_REACTION_NAME",
        ],
        [  # REACTION
            "NAME",
            "TYPE",
            "BACTERIANAME",
            "EQUATION",
            "RATECONSTANT",
            "GROWTH",
            "MONODTERMS",
            "THRESHHOLDTERMS",
            "INHIBITIONTERMS",
            "PRODUCTIONTERMS",
            "PRODUCTIONSTOCH",
            "BACTERIAL_YIELD",
            "ISOTOPE_FRACTIONATION",
            "BACTERIA_SPECIFIC_CAPACITY",
            "TEMPERATURE_DEPENDENCE",
            "_drmc_",
            "STANDARD_GIBBS_ENERGY",
            "EXCHANGE_PARAMETERS",
            "SORPTION_TYPE",
            "NAPL_PROPERTIES",
            "REACTION_ORDER",
            "MINERALNAME",
            "CHEMAPPNAME",
            "EQUILIBRIUM_CONSTANT",
            "RATE_EXPONENTS",
            "REACTIVE_SURFACE_AREA",
            "PRECIPITATION_BY_BASETERM_ONLY",
            "PRECIPITATION_FACTOR",
            "PRECIPITATION_EXPONENT",
            "BASETERM",
            "MECHANISMTERM",
            "SWITCH_OFF_GEOMETRY",
        ],
        [  # BLOB_PROPERTIES
            "NAME",
            "D50",
            #        "CALC_SHERWOOD",
            "DM",
            "DS",
            "UI",
            "NAPL_CONTENT_INI",
            "NAPL_CONTENT_RES",
            "GRAIN_SPHERE_RATIO",
            "TORTUOSITY",
            "LENGTH",
            "CALC_SHERWOOD",
            "CALC_SHERWOOD_MODIFIED",
            "SHERWOOD_MODEL",
            "GEOMETRY",
            "GAS_DISSOLUTION",
            "INTERFACIAL_AREA",
        ],
        [  # KINREACTIONDATA
            "SOLVER_TYPE",
            "RELATIVE_ERROR",
            "MIN_TIMESTEP",
            "INITIAL_TIMESTEP",
            "BACTERIACAPACITY",
            "MIN_BACTERIACONC",
            "MIN_CONCENTRATION_REPLACE",
            "SURFACES",
            "ALLOW_REACTIONS",
            "NO_REACTIONS",
            "COPY_CONCENTRATIONS",
            "LAGNEAU_BENCHMARK",
            "SCALE_DCDT",
            "SORT_NODES",
            "OMEGA_THRESHOLD",
            "REACTION_DEACTIVATION",
            "DEBUG_OUTPUT",
            "ACTIVITY_MODEL",
            "REALATIVE_ERROR",  # really?
            "MAX_TIMESTEP",  # really?
        ],
    ]

    STD = {}

    def __init__(self, **OGS_Config):
        super(KRC, self).__init__(**OGS_Config)
        self.file_ext = ".krc"

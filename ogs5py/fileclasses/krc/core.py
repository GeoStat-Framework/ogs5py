'''
Class for the ogs KINETRIC REACTION file.
'''

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import OGSfile


class KRC(OGSfile):
    """
    Class for the ogs KINETRIC REACTION file.

    Keywords for a block
    --------------------
    - BLOB_PROPERTIES
    - KINREACTIONDATA
    - MICROBE_PROPERTIES
    - REACTION
        - ACTIVITY_MODEL
        - ALLOW_REACTIONS
        - BACTERIACAPACITY
        - BACTERIAL_YIELD
        - BACTERIANAME
        - BACTERIA_SPECIFIC_CAPACITY
        - BASETERM
        - CALC_SHERWOOD
        - CALC_SHERWOOD_MODIFIED
        - CHEMAPPNAME
        - COPY_CONCENTRATIONS
        - D50
        - DEBUG_OUTPUT
        - DM
        - DS
        - EQUATION
        - EQUILIBRIUM_CONSTANT
        - EXCHANGE_PARAMETERS
        - GAS_DISSOLUTION
        - GEOMETRY
        - GRAIN_SPHERE_RATIO
        - GROWTH
        - INHIBITIONTERMS
        - INITIAL_TIMESTEP
        - INTERFACIAL_AREA
        - ISOTOPE_FRACTIONATION
        - LAGNEAU_BENCHMARK
        - LENGTH
        - MECHANISMTERM
        - MICROBENAME
        - MINERALNAME
        - MIN_BACTERIACONC
        - MIN_CONCENTRATION_REPLACE
        - MIN_TIMESTEP
        - MONODTERMS
        - MONOD_REACTION_NAME
        - NAME
        - NAPL_CONTENT_INI
        - NAPL_CONTENT_RES
        - NAPL_PROPERTIES
        - NO_REACTIONS
        - OMEGA_THRESHOLD
        - PRECIPITATION_BY_BASETERM_ONLY
        - PRECIPITATION_EXPONENT
        - PRECIPITATION_FACTOR
        - PRODUCTIONSTOCH
        - PRODUCTIONTERMS
        - RATECONSTANT
        - RATE_EXPONENTS
        - REACTION_DEACTIVATION
        - REACTION_ORDER
        - REACTIVE_SURFACE_AREA
        - RELATIVE_ERROR
        - SCALE_DCDT
        - SHERWOOD_MODEL
        - SOLVER_TYPE
        - SORPTION_TYPE
        - SORT_NODES
        - STANDARD_GIBBS_ENERGY
        - SURFACES
        - SWITCH_OFF_GEOMETRY
        - TEMPERATURE_DEPENDENCE
        - THRESHHOLDTERMS
        - TORTUOSITY
        - TYPE
        - UI
        - _drmc_
        - _drmc__PARAMETERS

    Standard block
    --------------
    None

    Info
    ----
    See: ``add_block``
    """

    MKEYS = ["BLOB_PROPERTIES",
             "KINREACTIONDATA",
             "MICROBE_PROPERTIES",
             "REACTION"]
    # these are not sorted at the moment
    SKEYS = 4*[["ACTIVITY_MODEL",
                "ALLOW_REACTIONS",
                "BACTERIACAPACITY",
                "BACTERIAL_YIELD",
                "BACTERIANAME",
                "BACTERIA_SPECIFIC_CAPACITY",
                "BASETERM",
                "CALC_SHERWOOD",
                "CALC_SHERWOOD_MODIFIED",
                "CHEMAPPNAME",
                "COPY_CONCENTRATIONS",
                "D50",
                "DEBUG_OUTPUT",
                "DM",
                "DS",
                "EQUATION",
                "EQUILIBRIUM_CONSTANT",
                "EXCHANGE_PARAMETERS",
                "GAS_DISSOLUTION",
                "GEOMETRY",
                "GRAIN_SPHERE_RATIO",
                "GROWTH",
                "INHIBITIONTERMS",
                "INITIAL_TIMESTEP",
                "INTERFACIAL_AREA",
                "ISOTOPE_FRACTIONATION",
                "LAGNEAU_BENCHMARK",
                "LENGTH",
                "MECHANISMTERM",
                "MICROBENAME",
                "MINERALNAME",
                "MIN_BACTERIACONC",
                "MIN_CONCENTRATION_REPLACE",
                "MIN_TIMESTEP",
                "MONODTERMS",
                "MONOD_REACTION_NAME",
                "NAME",
                "NAPL_CONTENT_INI",
                "NAPL_CONTENT_RES",
                "NAPL_PROPERTIES",
                "NO_REACTIONS",
                "OMEGA_THRESHOLD",
                "PRECIPITATION_BY_BASETERM_ONLY",
                "PRECIPITATION_EXPONENT",
                "PRECIPITATION_FACTOR",
                "PRODUCTIONSTOCH",
                "PRODUCTIONTERMS",
                "RATECONSTANT",
                "RATE_EXPONENTS",
                "REACTION_DEACTIVATION",
                "REACTION_ORDER",
                "REACTIVE_SURFACE_AREA",
                "RELATIVE_ERROR",
                "SCALE_DCDT",
                "SHERWOOD_MODEL",
                "SOLVER_TYPE",
                "SORPTION_TYPE",
                "SORT_NODES",
                "STANDARD_GIBBS_ENERGY",
                "SURFACES",
                "SWITCH_OFF_GEOMETRY",
                "TEMPERATURE_DEPENDENCE",
                "THRESHHOLDTERMS",
                "TORTUOSITY",
                "TYPE",
                "UI",
                "_drmc_",
                "_drmc__PARAMETERS"]]

    STD = {}

    def __init__(self, **OGS_Config):
        '''
        Input
        -----

        OGS_Config dictonary

        '''
        super(KRC, self).__init__(**OGS_Config)
        self.f_type = '.krc'

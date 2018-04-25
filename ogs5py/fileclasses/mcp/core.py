'''
Class for the ogs COMPONENT_PROPERTIES file.
'''

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import OGSfile


class MCP(OGSfile):
    """
    Class for the ogs COMPONENT_PROPERTIES file.

    Keywords for a block
    --------------------
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

    Standard block
    --------------
    None

    Info
    ----
    See: ``add_block``
    """

    MKEYS = ["COMPONENT_PROPERTIES"]
    SKEYS = [["ACENTRIC_FACTOR",
              "A_ZERO",
              "BUBBLE_VELOCITY",
              "CRITICAL_PRESSURE",
              "CRITICAL_TEMPERATURE",
              "DECAY",
              "DIFFUSION",
              "FLUID_ID",
              "FLUID_PHASE",
              "FORMULA",
              "ISOTHERM",
              "MAXIMUM_AQUEOUS_SOLUBILITY",
              "MINERAL_DENSITY",
              "MOBILE",
              "MOLAR_DENSITY",
              "MOLAR_VOLUME",
              "MOLAR_WEIGHT",
              "MOL_MASS",
              "NAME",
              "OutputMassOfComponentInModel",
              "TRANSPORT_PHASE",
              "VALENCE",
              "VOLUME_DIFFUSION"]]

    STD = {}

    def __init__(self, **OGS_Config):
        '''
        Input
        -----

        OGS_Config dictonary

        '''
        super(MCP, self).__init__(**OGS_Config)
        self.f_type = '.mcp'

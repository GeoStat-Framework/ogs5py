'''
Class for the ogs FLUID PROPERTY file.
'''

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import OGSfile


class MFP(OGSfile):
    """
    Class for the ogs FLUID PROPERTY file.

    Keywords for a block
    --------------------
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

    Standard block
    --------------
    :FLUID_TYPE: "LIQUID"
    :DENSITY: [[1, 1.0e+03]]
    :VISCOSITY: [[1, 1.0e-03]]

    Info
    ----
    See: ``add_block``
    """

    MKEYS = ["FLUID_PROPERTIES"]
    SKEYS = [["COMPONENTS",
              "COMPRESSIBILITY",
              "DAT_TYPE",
              "DECAY",
              "DENSITY",
              "DIFFUSION",
              "DRHO_DT_UNSATURATED",
              "EOS_TYPE",
              "FLUID_NAME",
              "FLUID_TYPE",
              "GRAVITY",
              "HEAT_CONDUCTIVITY",
              "ISOTHERM",
              "JTC",
              "NON_GRAVITY",
              "PHASE_DIFFUSION",
              "SPECIFIC_HEAT_CAPACITY",
              "SPECIFIC_HEAT_SOURCE",
              "TEMPERATURE",
              "VISCOSITY"]]

    STD = {"FLUID_TYPE": "LIQUID",
           "DENSITY": [[1, 1.0e+03]],
           "VISCOSITY": [[1, 1.0e-03]]}

    def __init__(self, **OGS_Config):
        '''
        Input
        -----

        OGS_Config dictonary

        '''
        super(MFP, self).__init__(**OGS_Config)
        self.f_type = '.mfp'

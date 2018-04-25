'''
Class for the ogs SOLID_PROPERTIES file.
'''

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import OGSfile


class MSP(OGSfile):
    """
    Class for the ogs SOLID_PROPERTIES file.

    Keywords for a block
    --------------------
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

    Standard block
    --------------
    None

    Info
    ----
    See: ``add_block``
    """

    MKEYS = ["SOLID_PROPERTIES"]
    SKEYS = [["BIOT_CONSTANT",
              "CREEP",
              "DENSITY",
              "ELASTICITY",
              "EXCAVATION",
              "E_Function",
              "GRAVITY_CONSTANT",
              "MICRO_STRUCTURE_PLAS",
              "NAME",
              "NON_REACTIVE_FRACTION",
              "PLASTICITY",
              "REACTIVE_SYSTEM",
              "SOLID_BULK_MODULUS",
              "SPECIFIC_HEAT_SOURCE",
              "STRESS_INTEGRATION_TOLERANCE",
              "STRESS_UNIT",
              "SWELLING_PRESSURE_TYPE",
              "THERMAL",
              "THRESHOLD_DEV_STR",
              "TIME_DEPENDENT_YOUNGS_POISSON"]]

    STD = {}

    def __init__(self, **OGS_Config):
        '''
        Input
        -----

        OGS_Config dictonary

        '''
        super(MSP, self).__init__(**OGS_Config)

        self.f_type = '.msp'

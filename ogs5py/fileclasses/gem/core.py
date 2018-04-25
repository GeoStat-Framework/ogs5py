'''
Class for the ogs GEOCHEMICAL THERMODYNAMIC MODELING COUPLING file.
'''

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import OGSfile


class GEM(OGSfile):
    """
    Class for the ogs GEOCHEMICAL THERMODYNAMIC MODELING COUPLING file.

    Keywords for a block
    --------------------
    - GEM_PROPERTIES
        - CALCULATE_BOUNDARY_NODES
        - DISABLE_GEMS
        - FLAG_COUPLING_HYDROLOGY
        - FLAG_DISABLE_GEM
        - FLAG_POROSITY_CHANGE
        - GEM_CALCULATE_BOUNDARY_NODES
        - GEM_INIT_FILE
        - GEM_THREADS
        - ITERATIVE_SCHEME
        - KINETIC_GEM
        - MAX_FAILED_NODES
        - MAX_POROSITY
        - MIN_POROSITY
        - MY_SMART_GEMS
        - PRESSURE_GEM
        - TEMPERATURE_GEM
        - TRANSPORT_B

    Standard block
    --------------
    None

    Info
    ----
    See: ``add_block``
    """

    MKEYS = ["GEM_PROPERTIES"]
    SKEYS = [["CALCULATE_BOUNDARY_NODES",
              "DISABLE_GEMS",
              "FLAG_COUPLING_HYDROLOGY",
              "FLAG_DISABLE_GEM",
              "FLAG_POROSITY_CHANGE",
              "GEM_CALCULATE_BOUNDARY_NODES",
              "GEM_INIT_FILE",
              "GEM_THREADS",
              "ITERATIVE_SCHEME",
              "KINETIC_GEM",
              "MAX_FAILED_NODES",
              "MAX_POROSITY",
              "MIN_POROSITY",
              "MY_SMART_GEMS",
              "PRESSURE_GEM",
              "TEMPERATURE_GEM",
              "TRANSPORT_B"]]

    STD = {}

    def __init__(self, **OGS_Config):
        '''
        Input
        -----

        OGS_Config dictonary

        '''
        super(GEM, self).__init__(**OGS_Config)
        self.f_type = '.gem'

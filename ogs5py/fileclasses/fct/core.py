'''
Class for the ogs FUNCTION file.
'''

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import OGSfile


class FCT(OGSfile):
    """
    Class for the ogs FUNCTION file.

    Keywords for a block
    --------------------
    - FUNCTION
        - DATA
        - DIMENSION
        - DIS_TYPE
        - GEO_TYPE
        - MATRIX
        - TYPE
        - VARIABLES

    Standard block
    --------------
    None

    Info
    ----
    See: ``add_block``
    """

    MKEYS = ["FUNCTION"]
    SKEYS = [["DATA",
              "DIMENSION",
              "DIS_TYPE",
              "GEO_TYPE",
              "MATRIX",
              "TYPE",
              "VARIABLES"]]

    STD = {}

    def __init__(self, **OGS_Config):
        '''
        Input
        -----

        OGS_Config dictonary

        '''
        super(FCT, self).__init__(**OGS_Config)
        self.f_type = '.fct'

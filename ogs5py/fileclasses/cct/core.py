'''
Class for the ogs COMMUNICATION TABLE file.
'''

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import OGSfile


class CCT(OGSfile):
    """
    Class for the ogs COMMUNICATION TABLE file.

    Keywords for a block
    --------------------
    - COMMUNICATION_TABLE
        - MYRANK
        - NEIGHBOR
        - NNEIGHBORS

    Standard block
    --------------
    None

    Info
    ----
    See: ``add_block``
    """

    MKEYS = ["COMMUNICATION_TABLE"]
    SKEYS = [["MYRANK",
              "NEIGHBOR",
              "NNEIGHBORS"]]

    STD = {}

    def __init__(self, **OGS_Config):
        '''
        Input
        -----

        OGS_Config dictonary

        '''
        super(CCT, self).__init__(**OGS_Config)
        self.f_type = '.cct'

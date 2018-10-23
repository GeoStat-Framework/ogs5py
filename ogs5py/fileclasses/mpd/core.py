'''
Class for the ogs MEDIUM_PROPERTIES_DISTRIBUTED file.
'''

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import OGSfile


class MPD(OGSfile):
    """
    Class for the ogs MEDIUM_PROPERTIES_DISTRIBUTED file.

    Keywords for a block
    --------------------
    - MEDIUM_PROPERTIES_DISTRIBUTED
        - MSH_TYPE
        - MMP_TYPE
        - DIS_TYPE
        - CONVERSION_FACTOR
        - DATA

    Standard block
    --------------
    None

    Info
    ----
    See: ``add_block``

    https://svn.ufz.de/ogs/wiki/public/doc-auto/by_ext/mmp

    https://github.com/ufz/ogs5/blob/master/FEM/rf_mmp_new.cpp#L5260
    """

    MKEYS = ["MEDIUM_PROPERTIES_DISTRIBUTED"]
    # sorted
    SKEYS = [[
        "MSH_TYPE",
        "MMP_TYPE",
        "DIS_TYPE",
        "CONVERSION_FACTOR",
        "DATA",
    ]]

    STD = {}

    def __init__(self, file_name=None, file_ext=".mpd", **OGS_Config):
        '''
        Input
        -----

        OGS_Config dictonary

        '''
        super(MPD, self).__init__(**OGS_Config)
        if file_name is None:
            file_name = self.task_id
        self.task_id = file_name
        self.f_type = file_ext
        self.top_com = None

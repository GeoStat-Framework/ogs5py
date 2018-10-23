'''
Class for the ogs TIME_STEPPING file.
'''

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import OGSfile


class TIM(OGSfile):
    """
    Class for the ogs TIME_STEPPING file.

    Keywords for a block
    --------------------
    - TIME_STEPPING
        - CRITICAL_TIME
        - INDEPENDENT
        - PCS_TYPE
        - SUBSTEPS
        - TIME_CONTROL
        - TIME_END
        - TIME_FIXED_POINTS
        - TIME_SPLITS
        - TIME_START
        - TIME_STEPS
        - TIME_UNIT

    Standard block
    --------------
    :PCS_TYPE: "GROUNDWATER_FLOW"
    :TIME_START: 0
    :TIME_END: 1000
    :TIME_STEPS: [[10, 100]]

    Info
    ----
    See: ``add_block``

    https://svn.ufz.de/ogs/wiki/public/doc-auto/by_ext/tim

    https://github.com/ufz/ogs5/blob/master/FEM/rf_tim_new.cpp#L161
    """

    MKEYS = ["TIME_STEPPING"]
    # sorted
    SKEYS = [[
        "PCS_TYPE",
        "TIME_START",
        "TIME_END",
        "TIME_UNIT",
        "INDEPENDENT",
        #        "TIME_FIXED_POINTS",
        "TIME_STEPS",
        "TIME_SPLITS",
        "CRITICAL_TIME",
        "TIME_CONTROL",
        #        "SUBSTEPS",
    ]]

    STD = {"PCS_TYPE": "GROUNDWATER_FLOW",
           "TIME_START": 0,
           "TIME_END": 1000,
           "TIME_STEPS": [10, 100]}

    def __init__(self, **OGS_Config):
        '''
        Input
        -----

        OGS_Config dictonary

        '''
        super(TIM, self).__init__(**OGS_Config)
        self.f_type = '.tim'

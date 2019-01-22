# -*- coding: utf-8 -*-
"""
Class for the ogs TIME_STEPPING file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import BlockFile


class TIM(BlockFile):
    """
    Class for the ogs TIME_STEPPING file.

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
        - TIME_STEPPING

    Sub-Keywords ($) per Main-Keyword:
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

    Standard block:
        :PCS_TYPE: "GROUNDWATER_FLOW"
        :TIME_START: 0
        :TIME_END: 1000
        :TIME_STEPS: [10, 100]

    Keyword documentation:
        https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/tim

    Reading routines:
        https://github.com/ufz/ogs5/blob/master/FEM/rf_tim_new.cpp#L161

    See Also
    --------
    add_block
    """

    MKEYS = ["TIME_STEPPING"]
    # sorted
    SKEYS = [
        [
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
        ]
    ]

    STD = {
        "PCS_TYPE": "GROUNDWATER_FLOW",
        "TIME_START": 0,
        "TIME_END": 1000,
        "TIME_STEPS": [10, 100],
    }

    def __init__(self, **OGS_Config):
        super(TIM, self).__init__(**OGS_Config)
        self.file_ext = ".tim"
        self.force_writing = True

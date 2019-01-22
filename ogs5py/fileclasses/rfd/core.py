# -*- coding: utf-8 -*-
"""
Class for the ogs USER DEFINED TIME CURVES file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import BlockFile


class RFD(BlockFile):
    """
    Class for the ogs USER DEFINED TIME CURVES file.

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
        - PROJECT
        - CURVE
        - CURVES

    Sub-Keywords ($) per Main-Keyword:
        (no sub-keywords)

    Standard block:
        None

    Keyword documentation:
        https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/rfd

    Reading routines:
        https://github.com/ufz/ogs5/blob/master/FEM/files0.cpp#L370

    See Also
    --------
    add_block
    """

    MKEYS = [
        "PROJECT",
        "CURVE",
        "CURVES",
        "RENUMBER",  # really?
        "ITERATION_PROPERTIES_CONCENTRATION",  # really?
        "REFERENCE_CONDITIONS",  # really?
        "APRIORI_REFINE_ELEMENT",  # really?
    ]
    # just a workaround in this case... since all content is related to mainkw
    SKEYS = [[""]] * len(MKEYS)

    STD = {}

    def __init__(self, **OGS_Config):
        super(RFD, self).__init__(**OGS_Config)
        self.file_ext = ".rfd"

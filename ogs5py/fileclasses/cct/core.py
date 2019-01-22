# -*- coding: utf-8 -*-
"""
Class for the ogs COMMUNICATION TABLE file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import BlockFile


class CCT(BlockFile):
    """
    Class for the ogs COMMUNICATION TABLE file.

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
        - COMMUNICATION_TABLE

    Sub-Keywords ($) per Main-Keyword:
        - COMMUNICATION_TABLE

            - MYRANK
            - NEIGHBOR
            - NNEIGHBORS

    Standard block:
        None

    Keyword documentation:
        https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/cct

    Reading routines:
        https://github.com/ufz/ogs5/blob/master/FEM/fct_mpi.cpp#L27

    See Also
    --------
    add_block
    """

    MKEYS = ["COMMUNICATION_TABLE"]
    # sorted
    SKEYS = [["MYRANK", "NNEIGHBORS", "NEIGHBOR"]]

    STD = {}

    def __init__(self, **OGS_Config):
        super(CCT, self).__init__(**OGS_Config)
        self.file_ext = ".cct"

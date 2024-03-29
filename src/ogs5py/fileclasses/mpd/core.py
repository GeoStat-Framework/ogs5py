# -*- coding: utf-8 -*-
"""Class for the ogs MEDIUM_PROPERTIES_DISTRIBUTED file."""
from ogs5py.fileclasses.base import BlockFile


class MPD(BlockFile):
    """
    Class for the ogs MEDIUM_PROPERTIES_DISTRIBUTED file.

    Parameters
    ----------
    name : str, optional
        File name for the MPD file. If :class:`None`, the task_id is used.
        Default: :class:`None`
    file_ext : :class:`str`, optional
        extension of the file (with leading dot ".mpd")
        Default: ".mpd"
    task_root : str, optional
        Path to the destiny model folder.
        Default: cwd+"ogs5model"
    task_id : str, optional
        Name for the ogs task.
        Default: "model"

    Notes
    -----
    Main-Keywords (#):
        - MEDIUM_PROPERTIES_DISTRIBUTED

    Sub-Keywords ($) per Main-Keyword:
        - MEDIUM_PROPERTIES_DISTRIBUTED

            - MSH_TYPE
            - MMP_TYPE
            - DIS_TYPE
            - CONVERSION_FACTOR
            - DATA

    Standard block:
        None

    Keyword documentation:
        https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/mmp

    Reading routines:
        https://github.com/ufz/ogs5/blob/master/FEM/rf_mmp_new.cpp#L5706

    See Also
    --------
    add_block
    """

    MKEYS = ["MEDIUM_PROPERTIES_DISTRIBUTED"]
    # sorted
    SKEYS = [["MSH_TYPE", "MMP_TYPE", "DIS_TYPE", "CONVERSION_FACTOR", "DATA"]]

    STD = {}

    def __init__(self, name=None, file_ext=".mpd", **OGS_Config):
        super().__init__(**OGS_Config)
        self.name = name
        self.file_ext = file_ext

    # no top comment allowed in the MPD file
    @property
    def top_com(self):
        """Top comment is 'None' for the MPD file."""
        return None

    @top_com.setter
    def top_com(self, val):
        pass

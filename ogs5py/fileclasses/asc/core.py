# -*- coding: utf-8 -*-
"""
Class for the ogs ASC file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import LineFile


class ASC(LineFile):
    """
    Class for the ogs ASC file.

    Parameters
    ----------
    lines : list of str, optional
        content of the file as a list of lines
        Default: None
    file_name : str, optional
        name of the file without extension
        Default: "textfile"
    task_root : str, optional
        Path to the destiny folder.
        Default: cwd+"ogs5model"
    task_id : str, optional
        Name for the ogs task. (a place holder)
        Default: "model"

    Notes
    -----
    This is just handled as a line-wise file. You can access the data by line
    with:

        ASC.lines

    This file type comes either from .tim .pcs or .gem
    """

    def __init__(self, **OGS_Config):
        super(ASC, self).__init__(**OGS_Config)
        self.file_ext = ".asc"

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
tools for the ogs5readerpy package

@author: sebastian
"""
from __future__ import division, print_function
import os


def split_file_path(path, abs_path=False):
    """
    decompose a path to a file into the dir-path, the basename
    and the file-extension

    Parameters
    ----------
    path : string
        string containing the path to a file
    abs_path: bool, optional
        convert the path to an absolut path. Default: False

    Returns
    -------
    result : tuple of strings
        tuple containing the dir-path, basename and file-extension
    """
    if abs_path:
        path = os.path.abspath(path)
    return os.path.split(path)[:1] + os.path.splitext(os.path.basename(path))

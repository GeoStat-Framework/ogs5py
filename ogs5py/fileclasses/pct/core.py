# -*- coding: utf-8 -*-
"""
Class for the ogs PARTICLE DEFINITION file for RANDOM_WALK.
"""

from __future__ import absolute_import, division, print_function
import os
import numpy as np
from ogs5py.fileclasses.base import File

CWD = os.getcwd()


class PCT(File):
    """
    Class for the ogs Particle file, if the PCS TYPE is RANDOM_WALK

    Parameters
    ----------
    data : np.array or None
        particle data. Default: None
    s_flag : int, optional
        1 for same pseudo-random series,
        0 for different pseudo-random series.
        Default: 1
    task_root : str, optional
        Path to the destiny model folder.
        Default: cwd+"ogs5model"
    task_id : str, optional
        Name for the ogs task.
        Default: "model"
    """

    def __init__(self, data=None, s_flag=1, task_root=CWD, task_id="model"):
        super(PCT, self).__init__(task_root, task_id)
        self.s_flag = s_flag
        self.file_ext = ".pct"
        if data:
            self.data = np.array(data)
        else:
            self.data = np.zeros((0, 10))

    @property
    def is_empty(self):
        """state if the OGS file is empty"""
        # check if the data is empty
        if self.check(False):
            return not self.data.shape[0] >= 1
        # if check is not passed, handle it as empty file
        return True

    def check(self, verbose=True):
        """
        Check if the external geometry definition is valid in the sence,
        that the contained data is consistent.

        Parameters
        ----------
        verbose : bool, optional
            Print information for the executed checks. Default: True

        Returns
        -------
        result : bool
            Validity of the given gli.
        """
        if self.data.ndim != 2:
            if verbose:
                print("PCT: Data shape incorect. Need 2 dimensions.")
            return False
        elif self.data.shape[1] != 10:
            if verbose:
                print("PCT: Data shape incorect. Need 10 columns.")
            return False
        return True

    def reset(self):
        """
        Delete every content.
        """
        self.data = np.zeros((0, 10))

    def save(self, path):
        """
        Save the actual PCT external file in the given path.

        Parameters
        ----------
        path : str
            path to where to file should be saved
        """
        if not self.is_empty:
            with open(path, "w") as fout:
                print(str(self.s_flag), file=fout)
                print(str(self.data.shape[0]), file=fout)
                np.savetxt(fout, self.data)

    def read_file(self, path, **kwargs):
        """
        Write the actual OGS input file to the given folder.
        Its path is given by "task_root+task_id+file_ext".
        """
        with open(path, "r") as fin:
            self.s_flag = int(fin.readline().split(";")[0].split()[0])
        # use numpy to read the data
        self.data = np.loadtxt(path, skiprows=2)

    def __repr__(self):
        out = str(self.s_flag) + "\n"
        out += str(self.data.shape[0]) + "\n"
        out += str(self.data)
        return out

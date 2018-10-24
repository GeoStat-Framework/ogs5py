'''
Class for the ogs PARTICLE DEFINITION file for RANDOM_WALK.
'''

from __future__ import absolute_import, division, print_function
import os
import numpy as np
import shutil

CWD = os.getcwd()


class PCT(object):
    """
    Class for the ogs Particle file, if the PCS TYPE is RANDOM_WALK
    """
    def __init__(self, data=None, s_flag=1, task_root=CWD, task_id="model"):
        '''
        Input
        -----
        data : np.array or None
            particle data. Default: None
        s_flag : int, optional
            1 for same pseudo-random series,
            0 for different pseudo-random series.
            Default: 1
        '''
        self.s_flag = s_flag
        self.task_root = task_root
        self.task_id = task_id
        self.f_type = ".pct"
        if data:
            self.data = np.array(data)
        else:
            self.data = np.zeros((0, 10))

        # if an existing file should be copied
        self.copy_file = None
        self.copy_path = None

    @property
    def is_empty(self):
        """state if the OGS file is empty"""
        # check if the list of main keywords is empty
        return not self.data.shape[0] >= 1

    def check(self, verbose=True):
        '''
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
        '''
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
        '''
        Delete every content.
        '''
        self.data = np.zeros((0, 10))

    def save(self, path):
        '''
        Save the actual PCT external file in the given path.

        Parameters
        ----------
        path : str
            path to where to file should be saved
        '''
        if not self.is_empty:
            with open(path, "w") as fout:
                print(str(self.s_flag), file=fout)
                print(str(self.data.shape[0]), file=fout)
                np.savetxt(fout, self.data)

    def read_file(self, path, **kwargs):
        '''
        Write the actual OGS input file to the given folder.
        Its path is given by "task_root+task_id+f_type".
        '''
        with open(path, "r") as fin:
                self.s_flag = int(fin.readline().split(";")[0].split()[0])
        # use numpy to read the data
        self.data = np.loadtxt(path, skiprows=2)

    def write_file(self):
        '''
        Write the actual OGS input file to the given folder.
        Its path is given by "task_root+task_id+f_type".
        '''
        # create the file path
        if not os.path.exists(self.task_root):
            os.makedirs(self.task_root)
        f_path = os.path.join(self.task_root, self.task_id+self.f_type)
        # check if we can copy the file or if we need to write it from data
        if self.copy_file is None:
            # if no content is present skip this file
            if not self.is_empty:
                self.save(f_path)
        # copy a given file if wanted
        elif self.copy_file == "copy":
            shutil.copyfile(self.copy_path, f_path)
        else:
            os.symlink(self.copy_path, f_path)

    def add_copy_link(self, path, symlink=False):
        '''
        Instead of writing a file, you can give a path to an existing file,
        that will be copied to the target folder

        Parameters
        ----------
        path : str
            path to the existing file that should be copied
        symlink : bool, optional
            on UNIX systems it is possible to use a symbolic link to save
            time if the file is big. Default: False
        '''
        if os.path.isfile(path):
            path = os.path.abspath(path)
            self.copy_file = "link" if symlink else "copy"
            self.copy_path = path
        else:
            print("ogs5py.PCT: Given copy-path is not a readable file: "+path)

    def del_copy_link(self):
        '''
        Remove a former given link to an external file.
        '''
        self.copy_file = None
        self.copy_path = None

    def __repr__(self):
        """
        Return a formatted representation of the file.

        Info
        ----
        Type : str
        """
        out = str(self.s_flag)+"\n"
        out += str(self.data.shape[0])+"\n"
        out += str(self.data)
        return out

    def __str__(self):
        """
        Return a formatted representation of the file.

        Info
        ----
        Type : str
        """
        return self.__repr__()

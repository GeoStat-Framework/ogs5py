# -*- coding: utf-8 -*-
"""
Class for the ogs INITIAL_CONDITION file.
"""

from __future__ import absolute_import, division, print_function
import os
import numpy as np
from ogs5py.fileclasses.base import BlockFile, File

CWD = os.getcwd()


class IC(BlockFile):
    """
    Class for the ogs INITIAL_CONDITION file.

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
        - INITIAL_CONDITION

    Sub-Keywords ($) per Main-Keyword:
        - INITIAL_CONDITION

            - COMP_NAME
            - DIS_TYPE
            - GEO_TYPE
            - PCS_TYPE
            - PRIMARY_VARIABLE
            - STORE_VALUES

    Standard block:
        :PCS_TYPE: "GROUNDWATER_FLOW"
        :PRIMARY_VARIABLE: "HEAD"
        :GEO_TYPE: "DOMAIN"
        :DIS_TYPE: ["CONSTANT", 0.0]

    Keyword documentation:
        https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/ic

    Reading routines:
        https://github.com/ufz/ogs5/blob/master/FEM/rf_ic_new.cpp#L222

    See Also
    --------
    add_block
    """

    MKEYS = ["INITIAL_CONDITION"]
    # sorted
    SKEYS = [
        [
            "PCS_TYPE",
            "PRIMARY_VARIABLE",
            "COMP_NAME",
            "STORE_VALUES",
            "DIS_TYPE",
            "GEO_TYPE",
        ]
    ]

    STD = {
        "PCS_TYPE": "GROUNDWATER_FLOW",
        "PRIMARY_VARIABLE": "HEAD",
        "GEO_TYPE": "DOMAIN",
        "DIS_TYPE": ["CONSTANT", 0.0],
    }

    def __init__(self, **OGS_Config):
        super(IC, self).__init__(**OGS_Config)
        self.file_ext = ".ic"


class RFR(File):
    """
    Class for the ogs RESTART file, if the DIS_TYPE in IC is set to RESTART

    Parameters
    ----------
    data : :any:`numpy.ndarray`, optional
        RFR data.
        Default: :class:`None`
    line1_4 : str or None, optional
        First four lines of the RFR file. If :class:`None`, a standard header
        is written.
        Default: :class:`None`
    file_name : str, optional
        File name for the RFR file. If :class:`None`, the task_id is used.
        Default: :class:`None`
    file_ext : :class:`str`, optional
        extension of the file (with leading dot ".rfr")
        Default: ".rfr"
    task_root : str, optional
        Path to the destiny model folder.
        Default: cwd+"ogs5model"
    task_id : str, optional
        Name for the ogs task.
        Default: "model"
    """

    def __init__(
        self,
        data=None,
        line1_4=None,
        file_name=None,
        file_ext=".rfr",
        task_root=os.path.join(CWD, "ogs5model"),
        task_id="model",
    ):
        super(RFR, self).__init__(task_root, task_id, file_ext)

        if line1_4 is None:
            line1_4 = [
                "#0#0#0#1#100000#0"
                + "#4.2.13 #########################################",
                "1 1 4",
                "1 1",
                "HEAD, m",
            ]
        self.line1_4 = line1_4

        if file_name is None:
            file_name = task_id
        self.file_name = file_name

        if data:
            self.data = np.array(data)
        else:
            self.data = np.zeros(0)

    @property
    def is_empty(self):
        """state if the OGS file is empty"""
        return bool(self.data.shape) and self.data.shape[0] > 0

    @property
    def file_path(self):
        """:class:`str`: save path of the file"""
        return os.path.join(self.task_root, self.file_name + self.file_ext)

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
        if self.data.ndim != 1:
            if verbose:
                print("RFR: Data shape incorrect")
            return False
        return True

    def save(self, path):
        """
        Save the actual RFR external file in the given path.

        Parameters
        ----------
        path : str
            path to where to file should be saved
        """
        if self.data.shape[0] >= 1:
            with open(path, "w") as fout:
                for line in self.line1_4:
                    print(line, file=fout)
                for data_i, data_e in enumerate(self.data):
                    print(str(data_i) + "\t" + str(data_e), file=fout)

    def read_file(self, path, encoding=None):
        """
        Write the actual RFR input file to the given folder.
        Its path is given by "task_root+task_id+file_ext".
        """
        # in python3 open was replaced with io.open
        from io import open

        with open(path, "r", encoding=encoding) as fin:
            lines = []
            for __ in range(4):
                lines.append(fin.readline().splitlines()[0])

        self.line1_4 = lines
        self.data = np.loadtxt(path, skiprows=4)[:, 1]

    def __repr__(self):
        out = ""
        for line in self.line1_4:
            out += line + "\n"
        for data_i, data_e in enumerate(self.data[:10]):
            out += str(data_i) + " " + str(data_e) + "\n"
        if len(self.data) > 10:
            out += "..."
        return out

# -*- coding: utf-8 -*-
"""
Class for the ogs DOMAIN DECOMPOSITION file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import BlockFile


class DDC(BlockFile):
    """
    Class for the ogs MPI DOMAIN DECOMPOSITION file.

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
        - DOMAIN

    Sub-Keywords ($) per Main-Keyword:
        - DOMAIN

            - ELEMENTS
            - NODES_INNER
            - NODES_BORDER

    Standard block:
        None

    Keyword documentation:
        None

    Reading routines:
        https://github.com/ufz/ogs5/blob/master/FEM/par_ddc.cpp

    See Also
    --------
    add_block
    """

    MKEYS = ["DOMAIN"]
    # sorted
    SKEYS = [["ELEMENTS", "NODES_INNER", "NODES_BORDER"]]

    STD = {}

    def __init__(self, **OGS_Config):
        super(DDC, self).__init__(**OGS_Config)
        self.file_ext = ".ddc"

    def save(self, path, **kwargs):
        """
        Save the actual DDC input file in the given path.

        Parameters
        ----------
        path : str
            path to where to file should be saved
        update : bool, optional
            state if the content should be updated before saving. Default: True
        """
        from ogs5py import SUB_IND, CON_IND

        if "update" in kwargs:
            update = bool(kwargs["update"])
        else:
            update = True
        # update the content
        if update:
            self._update_out()

        # open the file
        with open(path, "w") as fout:
            # iterate over the main keywords
            for i, mkw in enumerate(self.mainkw):
                # the number of the actual DOMAIN is behind the main key
                print("#" + mkw, i, sep=" ", file=fout)
                # iterate over the subkeywords
                for j, skw in enumerate(self.subkw[i]):
                    # the number of related content is behind the sub key
                    print(
                        SUB_IND + "$" + skw,
                        len(self.cont[i][j]),
                        sep=" ",
                        file=fout,
                    )
                    # iterate over the content
                    for con in self.cont[i][j]:
                        if CON_IND:
                            print(
                                CON_IND[:-1],  # hack to fit with sep=" "
                                *con,
                                sep=" ",
                                file=fout
                            )
                        else:
                            print(*con, sep=" ", file=fout)
            # write the final STOP keyword
            if self.bot_com:
                print("#STOP", file=fout)
                print(self.bot_com, end="", file=fout)
            else:
                print("#STOP", end="", file=fout)

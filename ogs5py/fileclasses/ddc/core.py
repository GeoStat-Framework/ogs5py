"""
Class for the ogs DOMAIN DECOMPOSITION file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import OGSfile


class DDC(OGSfile):
    """
    Class for the ogs MPI DOMAIN DECOMPOSITION file.

    Keywords for a block
    --------------------
    - DOMAIN
        - ELEMENTS
        - NODES_INNER
        - NODES_BORDER

    Standard block
    --------------
    None

    Info
    ----
    See: ``add_block``

    https://github.com/ufz/ogs5/blob/master/FEM/par_ddc.cpp
    """

    MKEYS = ["DOMAIN"]
    # sorted
    SKEYS = [["ELEMENTS", "NODES_INNER", "NODES_BORDER"]]

    STD = {}

    def __init__(
        self,
        # count=None,
        **OGS_Config
    ):
        """
        Input
        -----

        OGS_Config dictonary

        """
        super(DDC, self).__init__(**OGS_Config)

    #        self.count = count
    #
    #    @property
    #    def file_ext(self):
    #        if self.count is None or self.count <= 1:
    #            return '.ddc'
    #        return '.'+str(self.count)+'ddc'
    #
    #    @file_ext.setter
    #    def file_ext(self, val):
    #        pass

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

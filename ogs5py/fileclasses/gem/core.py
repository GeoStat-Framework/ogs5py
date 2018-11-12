"""
Class for the ogs GEOCHEMICAL THERMODYNAMIC MODELING COUPLING file.
"""

from __future__ import absolute_import, division, print_function
import os
from copy import deepcopy
from ogs5py.fileclasses.base import OGSfile, LineFile

# current working directory
CWD = os.getcwd()


class GEM(OGSfile):
    """
    Class for the ogs GEOCHEMICAL THERMODYNAMIC MODELING COUPLING file.

    Keywords for a block
    --------------------
    - GEM_PROPERTIES
        - CALCULATE_BOUNDARY_NODES
        - DISABLE_GEMS
        - FLAG_COUPLING_HYDROLOGY
        - FLAG_DISABLE_GEM
        - FLAG_POROSITY_CHANGE
        - GEM_CALCULATE_BOUNDARY_NODES
        - GEM_INIT_FILE
        - GEM_THREADS
        - ITERATIVE_SCHEME
        - KINETIC_GEM
        - MAX_FAILED_NODES
        - MAX_POROSITY
        - MIN_POROSITY
        - MY_SMART_GEMS
        - PRESSURE_GEM
        - TEMPERATURE_GEM
        - TRANSPORT_B

    Standard block
    --------------
    None

    Info
    ----
    See: ``add_block``

    https://svn.ufz.de/ogs/wiki/public/doc-auto/by_ext/gem

    https://github.com/ufz/ogs5/blob/master/FEM/rf_REACT_GEM.cpp#L2644
    """

    MKEYS = ["GEM_PROPERTIES"]
    # sorted
    SKEYS = [
        [
            "GEM_INIT_FILE",
            "GEM_THREADS",
            "TRANSPORT_B",
            "FLAG_POROSITY_CHANGE",
            "MIN_POROSITY",
            "MAX_POROSITY",
            "FLAG_COUPLING_HYDROLOGY",
            "ITERATIVE_SCHEME",
            "CALCULATE_BOUNDARY_NODES",
            "TEMPERATURE_GEM",
            "PRESSURE_GEM",
            "MAX_FAILED_NODES",
            "MY_SMART_GEMS",
            "FLAG_DISABLE_GEM",
            "KINETIC_GEM",
            #        "DISABLE_GEMS",
            #        "GEM_CALCULATE_BOUNDARY_NODES",
        ]
    ]

    STD = {}

    def __init__(self, **OGS_Config):
        """
        Input
        -----

        OGS_Config dictonary

        """
        super(GEM, self).__init__(**OGS_Config)
        self.file_ext = ".gem"


class GEMext(object):
    """
    Class for an external definition for the ogs GEOMETRY file.

    Attributes
    ----------
    task_root : string
        the task root folder
    lst_name : string
        the file-name of the GEM lst file
    files : list of LineFiles
        list of the given files as LineFile-Classes
    is_empty : bool
        state of the file is empty
    """

    def __init__(
        self,
        task_root=os.path.join(CWD, "ogs5model"),
        lst_name="model-dat.lst",
        files=None,
    ):
        """
        Input
        -----
        lst_name: string
            name of the lst file
        """
        self.task_root = task_root
        self.lst_name = lst_name
        if files is not None:
            self.files = files
        else:
            self.files = []

    def get_file_type(self):
        """Get the OGS file class name"""
        return "lst"

    @property
    def is_empty(self):
        """state if the file is empty"""
        # check if the list of main keywords is empty
        if self.check(False):
            return not bool(self.files)
        # if check is not passed, handle it as empty file
        return True

    def reset(self):
        """
        Delete every content.
        """
        self.files = []

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
        # no checks are performed
        return True

    def save(self, path):
        """
        Save the actual GEM external file in the given path.
        lst - dch - ipm - dbr

        Parameters
        ----------
        path : str
            path to where to file should be saved
        """
        for file in self.files:
            file.write_file()
        with open(path, "w") as fout:
            fout.write(str(self))

    def read_file(self, path, encoding=None, verbose=False):
        """
        Read a given GEM external input lst-file.

        Parameters
        ----------
        path : str
            path to the file

        Note
        ----
        This also reads the given files in the lst-file. (dch, ipm, dbr)
        """
        # in python3 open was replaced with io.open
        # so we can use encoding key word in python2
        from io import open

        root = os.path.dirname(path)

        self.reset()
        try:
            with open(path, "r", encoding=encoding) as fin:
                for line in fin:
                    if line.strip().startswith("-t"):
                        file_names = []
                        for file_name in line.strip().split()[1:]:
                            file_names.append(file_name.strip('"').strip("'"))
                        break
        except IOError:
            if verbose:
                print(
                    "ogs5py "
                    + self.get_file_type()
                    + ": could not read lst-file: "
                    + path
                )
        else:
            for file_name in file_names:
                file_cl = LineFile(
                    file_name=os.path.splitext(file_name)[0],
                    file_ext=os.path.splitext(file_name)[1],
                    task_root=self.task_root,
                )
                file_cl.read_file(
                    path=os.path.join(root, file_name),
                    encoding=encoding,
                    verbose=verbose,
                )
                self.files.append(deepcopy(file_cl))

    def write_file(self):
        """
        Write the actual OGS input file to the given folder.
        Its path is given by "task_root+task_id+file_ext".
        """
        # create the file path
        if not os.path.exists(self.task_root):
            os.makedirs(self.task_root)
        f_path = os.path.join(self.task_root, self.lst_name)
        # save the data
        if not self.is_empty:
            self.save(f_path)

    def __repr__(self):
        """
        Return a formatted representation of the file.

        Info
        ----
        Type : str
        """
        out_str = "-t"
        for file in self.files:
            out_str += ' "' + file.file_name + file.file_ext + '"'
        return out_str

    def __str__(self):
        """
        Return a formatted representation of the file.

        Info
        ----
        Type : str
        """
        return self.__repr__()

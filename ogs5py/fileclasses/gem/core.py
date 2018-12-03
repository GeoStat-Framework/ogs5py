"""
Class for the ogs GEOCHEMICAL THERMODYNAMIC MODELING COUPLING file.
"""

from __future__ import absolute_import, division, print_function
import os
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

    https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/gem

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


class GEMinit(object):
    """
    Class for GEMS3K input file (lst file) that contains the names of

        * the GEMS data file (dch file),
        * the GEMS numerical settings (ipm file)
        * the example setup (dbr file)

    used to initialize the GEMS3K kernel.

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

    Info
    ----
    http://gems.web.psi.ch/GEMS3/index.html

    http://gems.web.psi.ch/GEMS3K/

    http://gems.web.psi.ch/GEMS3K/doc/html/gems3k-iofiles.html
    """

    def __init__(
        self,
        lst_name="model-dat.lst",
        dch=None,
        ipm=None,
        dbr=None,
        task_root=os.path.join(CWD, "ogs5model"),
        task_id="model",
    ):
        """
        Input
        -----
        lst_name: string
            name of the lst file
        dch: LineFile or None
            the GEMS data file
        ipm: LineFile or None
            the GEMS data file
        dbr: LineFile or None
            the GEMS data file
        task_root : str
            Path to the destiny folder.
        """
        self._task_root = task_root
        self.task_id = task_id
        self.lst_name = lst_name
        # add files
        if dch is not None:
            self.dch = dch
        else:
            self.dch = LineFile(
                file_name=self.task_id + "-dch",
                file_ext=".dat",
                task_root=self.task_root,
            )
        if ipm is not None:
            self.ipm = ipm
        else:
            self.ipm = LineFile(
                file_name=self.task_id + "-ipm",
                file_ext=".dat",
                task_root=self.task_root,
            )
        if dbr is not None:
            self.dbr = dbr
        else:
            self.dbr = LineFile(
                file_name=self.task_id + "-dbr",
                file_ext=".dat",
                task_root=self.task_root,
            )

    def get_file_type(self):
        """Get the OGS file class name"""
        return "lst"

    @property
    def files(self):
        """
        List of the included files: dch, ipm, dbr.
        """
        out_list = []
        if self.dch is not None:
            out_list.append(self.dch)
        if self.ipm is not None:
            out_list.append(self.ipm)
        if self.dbr is not None:
            out_list.append(self.dbr)
        return out_list

    @property
    def file_names(self):
        """
        The names of the included files.
        """
        out_list = []
        for file in self.files:
            out_list.append(file.file_name + file.file_ext)
        return out_list

    def __bool__(self):
        return not self.is_empty

    def __nonzero__(self):
        return self.__bool__()

    @property
    def is_empty(self):
        """state if the file is empty"""
        # check if the files are empty
        if self.check(False):
            return not any(self.files)
        # if check is not passed, handle it as empty file
        return True

    @property
    def task_root(self):
        """
        Get and set the task_root path of the ogs model.
        """
        return self._task_root

    @task_root.setter
    def task_root(self, value):
        self._task_root = value
        self.dch.task_root = value
        self.ipm.task_root = value
        self.dbr.task_root = value

    def reset(self):
        """
        Delete every content.
        """
        self.dch = LineFile(
            file_name=self.task_id + "-dch",
            file_ext=".dat",
            task_root=self.task_root,
        )
        self.ipm = LineFile(
            file_name=self.task_id + "-ipm",
            file_ext=".dat",
            task_root=self.task_root,
        )
        self.dbr = LineFile(
            file_name=self.task_id + "-dbr",
            file_ext=".dat",
            task_root=self.task_root,
        )

    def check(self, verbose=True):
        """
        Check if the GEM external file is valid.

        Parameters
        ----------
        verbose : bool, optional
            Print information for the executed checks. Default: True

        Returns
        -------
        result : bool
            Validity.
        """
        # no checks are performed
        out = True
        for file in self.files:
            out &= file.check(verbose)
        return out

    def save(self, path):
        """
        Save the actual GEM external file in the given path.
        lst file containing: dch, ipm, dbr

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
                        # get rid of leading "-t"
                        for file_name in line.split()[1:]:
                            # get rid of " and ' around strings
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
            # hard coded order of files
            self.dch.file_name = os.path.splitext(file_names[0])[0]
            self.dch.file_ext = os.path.splitext(file_names[0])[1]
            self.dch.read_file(
                path=os.path.join(root, file_names[0]),
                encoding=encoding,
                verbose=verbose,
            )
            self.ipm.file_name = os.path.splitext(file_names[1])[0]
            self.ipm.file_ext = os.path.splitext(file_names[1])[1]
            self.ipm.read_file(
                path=os.path.join(root, file_names[1]),
                encoding=encoding,
                verbose=verbose,
            )
            self.dbr.file_name = os.path.splitext(file_names[2])[0]
            self.dbr.file_ext = os.path.splitext(file_names[2])[1]
            self.dbr.read_file(
                path=os.path.join(root, file_names[2]),
                encoding=encoding,
                verbose=verbose,
            )

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
        for file_name in self.file_names:
            out_str += ' "' + file_name + '"'
        return out_str

    def __str__(self):
        """
        Return a formatted representation of the file.

        Info
        ----
        Type : str
        """
        return self.__repr__()

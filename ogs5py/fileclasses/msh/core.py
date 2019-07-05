# -*- coding: utf-8 -*-
"""
core module for the ogs5py-mesh package.
Containing the classes for the OGS5 mesh files.
"""

from __future__ import division, print_function, absolute_import
from copy import deepcopy as dcp
import numpy as np
from ogs5py.fileclasses.msh import generator as gen
from ogs5py.tools.types import ELEM_NAMES, EMPTY_MSH
from ogs5py.fileclasses.msh.checker import check_mesh_list, check_mesh_dict
from ogs5py.fileclasses.msh.tools import (
    load_ogs5msh,
    save_ogs5msh,
    import_mesh,
    export_mesh,
    combine,
    get_centroids,
    get_volumes,
    remove_dim,
    gen_std_elem_id,
    gen_std_mat_id,
    rotate_mesh,
    shift_mesh,
    transform_mesh,
    no_of_elements,
)
from ogs5py.fileclasses.base import File


class MSHsgl(File):
    """
    Class for a single mesh file.

    Parameters
    ----------
    mesh_dict : dict or None, optional
        Dictionary contains one '#FEM_MSH' block of the mesh file with
        the following information (sorted by keys):
            - mesh_data : dictionary
                contains information about (sorted by keys):
                    - AXISYMMETRY: bool (just true, otherwise not present)
                    - CROSS_SECTION: bool (just true, otherwise not present)
                    - PCS_TYPE: string
                    - GEO_TYPE: str
                    - GEO_NAME: string
                    - LAYER: int
            - nodes : ndarray
                Array with all node postions
            - elements : dictionary
                contains array of nodelists for elements sorted by element type
            - material_id : dictionary
                contains material ids for each element sorted by element type
    task_root : str, optional
        Path to the destiny model folder.
        Default: cwd+"ogs5model"
    task_id : str, optional
        Name for the ogs task.
        Default: "model"
    """

    def __init__(self, mesh_dict=None, **OGS_Config):
        super(MSHsgl, self).__init__(**OGS_Config)
        self.file_ext = ".msh"
        self.force_writing = True

        if mesh_dict is None:
            self.__dict = EMPTY_MSH
        else:
            if isinstance(mesh_dict, list):
                raise ValueError(
                    "The given mesh may contains a multi-layer "
                    + "mesh. Try loading within "
                    + "the multimesh class."
                )
            else:
                if check_mesh_dict(mesh_dict):
                    self.__dict = mesh_dict
                else:
                    print("given mesh is not valid")
        self._block = 0

    # Pretend that there is a main keyword in the standard BASE-FORMAT
    @property
    def is_empty(self):
        return not bool(self._meshlist[0]["elements"])

    #######################
    ### meshlist
    #######################
    # this is a workaround to make multi-layer and single-layer meshes usable
    @property
    def _meshlist(self):
        """list: mesh as list of dicts"""
        return [self._dict]

    @_meshlist.setter
    def _meshlist(self, value):
        self._dict = value[0]

    @_meshlist.deleter
    def _meshlist(self):
        self._dict = EMPTY_MSH

    @property
    def _dict(self):
        return self.__dict

    @_dict.setter
    def _dict(self, value):
        self.__dict = value

    #######################
    ### AXISYMMETRY
    #######################
    @property
    def AXISYMMETRY(self):
        """bool: AXISYMMETRY attribute."""
        if "AXISYMMETRY" in self._dict["mesh_data"]:
            return self._dict["mesh_data"]["AXISYMMETRY"]
        return False

    @AXISYMMETRY.setter
    def AXISYMMETRY(self, value):
        if value:
            self._dict["mesh_data"]["AXISYMMETRY"] = True
        else:
            del self.AXISYMMETRY

    @AXISYMMETRY.deleter
    def AXISYMMETRY(self):
        if "AXISYMMETRY" in self._dict["mesh_data"]:
            del self._dict["mesh_data"]["AXISYMMETRY"]

    #######################
    ### CROSS_SECTION
    #######################
    @property
    def CROSS_SECTION(self):
        """bool: CROSS_SECTION attribute."""
        if "CROSS_SECTION" in self._dict["mesh_data"]:
            return self._dict["mesh_data"]["CROSS_SECTION"]
        return False

    @CROSS_SECTION.setter
    def CROSS_SECTION(self, value):
        if value:
            self._dict["mesh_data"]["CROSS_SECTION"] = True
        else:
            del self.CROSS_SECTION

    @CROSS_SECTION.deleter
    def CROSS_SECTION(self):
        if "CROSS_SECTION" in self._dict["mesh_data"]:
            del self._dict["mesh_data"]["CROSS_SECTION"]

    #######################
    ### PCS_TYPE
    #######################
    @property
    def PCS_TYPE(self):
        """str: PCS_TYPE"""
        if "PCS_TYPE" in self._dict["mesh_data"]:
            return self._dict["mesh_data"]["PCS_TYPE"]
        return None

    @PCS_TYPE.setter
    def PCS_TYPE(self, value):
        if value is not None:
            value = str(value)
        if value:
            self._dict["mesh_data"]["PCS_TYPE"] = value
        else:
            del self.PCS_TYPE

    @PCS_TYPE.deleter
    def PCS_TYPE(self):
        if "PCS_TYPE" in self._dict["mesh_data"]:
            del self._dict["mesh_data"]["PCS_TYPE"]

    #######################
    ### GEO_NAME
    #######################
    @property
    def GEO_NAME(self):
        """str: GEO_NAME"""
        if "GEO_NAME" in self._dict["mesh_data"]:
            return self._dict["mesh_data"]["GEO_NAME"]
        return None

    @GEO_NAME.setter
    def GEO_NAME(self, value):
        if value is not None:
            value = str(value)
        if value:
            self._dict["mesh_data"]["GEO_NAME"] = value
        else:
            del self.GEO_NAME

    @GEO_NAME.deleter
    def GEO_NAME(self):
        if "GEO_NAME" in self._dict["mesh_data"]:
            del self._dict["mesh_data"]["GEO_NAME"]
            del self.GEO_TYPE

    #######################
    ### GEO_TYPE
    #######################
    @property
    def GEO_TYPE(self):
        """str: GEO_TYPE"""
        if "GEO_TYPE" in self._dict["mesh_data"]:
            return self._dict["mesh_data"]["GEO_TYPE"]
        return None

    @GEO_TYPE.setter
    def GEO_TYPE(self, value):
        if value is not None:
            value = str(value)
        if value:
            self._dict["mesh_data"]["GEO_TYPE"] = value
        else:
            del self.GEO_TYPE

    @GEO_TYPE.deleter
    def GEO_TYPE(self):
        if "GEO_TYPE" in self._dict["mesh_data"]:
            del self._dict["mesh_data"]["GEO_TYPE"]

    #######################
    ### LAYER
    #######################
    @property
    def LAYER(self):
        """int: LAYER"""
        if "LAYER" in self._dict["mesh_data"]:
            return self._dict["mesh_data"]["LAYER"]
        return None

    @LAYER.setter
    def LAYER(self, value):
        if value is not None:
            self._dict["mesh_data"]["LAYER"] = int(value)
        else:
            del self.LAYER

    @LAYER.deleter
    def LAYER(self):
        if "LAYER" in self._dict["mesh_data"]:
            del self._dict["mesh_data"]["LAYER"]

    #######################
    ### NODES
    #######################
    @property
    def NODES(self):
        """ndarray: (n,3) NODES of the mesh by its xyz-coordinates"""
        return self._dict["nodes"]

    @NODES.setter
    def NODES(self, value):
        self._dict["nodes"] = np.array(value)

    @NODES.deleter
    def NODES(self):
        self._dict["nodes"] = None
        del self.ELEMENTS
        del self.MATERIAL_ID
        del self.ELEMENT_ID

    #######################
    ### ELEMENTS
    #######################
    @property
    def ELEMENTS(self):
        """
        Get and set the ELEMENTS of the mesh.

        Notes
        -----
        Type : dict of ndarrays
            The elements are a dictionary sorted by their element-type

                "line" : ndarray of shape (n_line,2)
                    1D element with 2 nodes
                "tri" : ndarray of shape (n_tri,3)
                    2D element with 3 nodes
                "quad" : ndarray of shape (n_quad,4)
                    2D element with 4 nodes
                "tet" : ndarray of shape (n_tet,4)
                    3D element with 4 nodes
                "pyra" : ndarray of shape (n_pyra,5)
                    3D element with 5 nodes
                "pris" : ndarray of shape (n_pris,6)
                    3D element with 6 nodes
                "hex" : ndarray of shape (n_hex,8)
                    3D element with 8 nodes
        """
        return self._dict["elements"]

    @ELEMENTS.setter
    def ELEMENTS(self, value):
        self._dict["elements"] = value

    @ELEMENTS.deleter
    def ELEMENTS(self):
        self._dict["elements"] = {}
        del self.MATERIAL_ID
        del self.ELEMENT_ID

    #######################
    ### MATERIAL_ID
    #######################
    @property
    def MATERIAL_ID(self):
        """
        Get and set the MATERIAL_IDs of the mesh.

        Notes
        -----
        Type : dict of ndarrays
            The material IDs are a dictionary containing ints
            sorted by their element-type

                "line" : ndarray of shape (n_line,)
                    1D element with 2 nodes
                "tri" : ndarray of shape (n_tri,)
                    2D element with 3 nodes
                "quad" : ndarray of shape (n_quad,)
                    2D element with 4 nodes
                "tet" : ndarray of shape (n_tet,)
                    3D element with 4 nodes
                "pyra" : ndarray of shape (n_pyra,)
                    3D element with 5 nodes
                "pris" : ndarray of shape (n_pris,)
                    3D element with 6 nodes
                "hex" : ndarray of shape (n_hex,)
                    3D element with 8 nodes
        """
        return self._dict["material_id"]

    @MATERIAL_ID.setter
    def MATERIAL_ID(self, value):
        if isinstance(value, int):
            self._dict["material_id"] = gen_std_mat_id(self.ELEMENTS, value)
        else:
            self._dict["material_id"] = value

    @MATERIAL_ID.deleter
    def MATERIAL_ID(self):
        self._dict["material_id"] = gen_std_mat_id(self.ELEMENTS)

    @property
    def MATERIAL_ID_flat(self):
        """
        Get flat version of the MATERIAL_IDs of the mesh.

        See "mesh.MATERIAL_ID"
        This flattend MATERIAL_IDs are a stacked version of MATERIAL_ID, to get
        one continous array. They are stacked in order of the ELEMENT_IDs.
        Standard stack order is given by:

            "line" "tri" "quad" "tet" "pyra" "pris" "hex"

        Notes
        -----
        Type : ndarray
            The centroids are a list containing xyz-coordiantes
        """
        # just call centroids once
        tmp = dcp(self.MATERIAL_ID)
        out = np.empty(self.ELEMENT_NO, dtype=int)
        for elem in ELEM_NAMES:
            if elem not in self.ELEMENTS:
                continue
            out[self.ELEMENT_ID[elem]] = tmp[elem]
        return out

    #######################
    ### ELEMENT_ID
    #######################
    @property
    def ELEMENT_ID(self):
        """
        Get and set the ELEMENT_IDs of the mesh.
        Standard element id order is given by:

            "line" "tri" "quad" "tet" "pyra" "pris" "hex"

        Notes
        -----
        Type : dict of ndarrays
            The element IDs are a dictionary containing ints
            sorted by their element-type

                "line" : ndarray of shape (n_line,)
                    1D element with 2 nodes
                "tri" : ndarray of shape (n_tri,)
                    2D element with 3 nodes
                "quad" : ndarray of shape (n_quad,)
                    2D element with 4 nodes
                "tet" : ndarray of shape (n_tet,)
                    3D element with 4 nodes
                "pyra" : ndarray of shape (n_pyra,)
                    3D element with 5 nodes
                "pris" : ndarray of shape (n_pris,)
                    3D element with 6 nodes
                "hex" : ndarray of shape (n_hex,)
                    3D element with 8 nodes
        """
        return self._dict["element_id"]

    @ELEMENT_ID.setter
    def ELEMENT_ID(self, value):
        self._dict["element_id"] = value

    @ELEMENT_ID.deleter
    def ELEMENT_ID(self):
        self._dict["element_id"] = gen_std_elem_id(self.ELEMENTS)

    #######################
    ### ELEMENT_NO
    #######################
    @property
    def ELEMENT_NO(self):
        """int: number of ELEMENTS"""
        return no_of_elements(self._dict)

    #######################
    ### NODE_NO
    #######################
    @property
    def NODE_NO(self):
        """int: number of NODES"""
        if self.NODES is None:
            return 0
        return self.NODES.shape[0]

    #######################
    ### centroids
    #######################
    @property
    def centroids(self):
        """
        Get the centroids of the mesh.

        Notes
        -----
        Type : dict of ndarrays
            The centroids are a dictionary containing xyz-coordiantes
            sorted by their element-type

                "line" : ndarray of shape (n_line,3)
                    1D element with 2 nodes
                "tri" : ndarray of shape (n_tri,3)
                    2D element with 3 nodes
                "quad" : ndarray of shape (n_quad,3)
                    2D element with 4 nodes
                "tet" : ndarray of shape (n_tet,3)
                    3D element with 4 nodes
                "pyra" : ndarray of shape (n_pyra,3)
                    3D element with 5 nodes
                "pris" : ndarray of shape (n_pris,3)
                    3D element with 6 nodes
                "hex" : ndarray of shape (n_hex,3)
                    3D element with 8 nodes
        """
        return get_centroids(self._dict)

    @property
    def centroids_flat(self):
        """
        Get flat version of the centroids of the mesh.

        See the "mesh.get_centroids" method.
        This flattend centroids are a stacked version of centroids, to get
        one continous array. They are stacked in order of the element ids.
        Standard stack order is given by:

            "line" "tri" "quad" "tet" "pyra" "pris" "hex"

        Notes
        -----
        Type : ndarray
            The centroids are a list containing xyz-coordiantes
        """
        # just call centroids once
        tmp = dcp(self.centroids)
        out = np.empty((self.ELEMENT_NO, 3), dtype=float)
        for elem in ELEM_NAMES:
            if elem not in self.ELEMENTS:
                continue
            out[self.ELEMENT_ID[elem]] = tmp[elem]
        return out

    #######################
    ### volumes
    #######################
    @property
    def volumes(self):
        """
        Get the volumes of the mesh-elements.

        Notes
        -----
        Type : dict of ndarrays
            The volumes are a dictionary containing the n-dimension volumes
            sorted by their element-type

                "line" : ndarray of shape (n_line,3)
                    1D element with 2 nodes
                "tri" : ndarray of shape (n_tri,3)
                    2D element with 3 nodes
                "quad" : ndarray of shape (n_quad,3)
                    2D element with 4 nodes
                "tet" : ndarray of shape (n_tet,3)
                    3D element with 4 nodes
                "pyra" : ndarray of shape (n_pyra,3)
                    3D element with 5 nodes
                "pris" : ndarray of shape (n_pris,3)
                    3D element with 6 nodes
                "hex" : ndarray of shape (n_hex,3)
                    3D element with 8 nodes
        """
        return get_volumes(self._dict)

    @property
    def volumes_flat(self):
        """
        Get flat version of the volumes of the mesh-elements.

        This flattend volumes are a stacked version of centroids, to get
        one continous array. They are stacked in order of the element ids.
        Standard stack order is given by:

            "line" "tri" "quad" "tet" "pyra" "pris" "hex"

        Notes
        -----
        Type : ndarray
            The volumes are a list containing the n-dimensional element volume
        """
        # just call volumes once
        tmp = dcp(self.volumes)
        out = np.empty(self.ELEMENT_NO, dtype=float)
        for elem in ELEM_NAMES:
            if elem not in self.ELEMENTS:
                continue
            out[self.ELEMENT_ID[elem]] = tmp[elem]
        return out

    #######################
    ### Class methods
    #######################
    def reset(self):
        """
        Delete every content.
        """
        self._block = 0
        self._meshlist = [EMPTY_MSH]

    def load(self, filepath, **kwargs):
        """
        Load an OGS5 mesh from file.
        kwargs will be forwarded to "tools.load_ogs5msh"

        Parameters
        ----------
        filepath : string
            path to the '\*.msh' OGS5 mesh file to load
        verbose : bool, optional
            Print information of the reading process. Default: True
        ignore_unknown : bool, optional
            Unknown data in the file will be ignored. Default: False
        max_node_no : int, optional
            If you know the maximal node number per elements in the mesh file,
            you can optimise the reading a bit. By default the algorithm will
            assume hexahedrons as 'largest' elements in the mesh. Default: 8
        encoding : str or None, optional
            encoding of the given file. If ``None`` is given, the system
            standard is used. Default: ``None``

        Notes
        -----
        The $AREA keyword within the Nodes definition is NOT supported
        and will violate the read data if present.
        """
        #        kwargs["verbose"] = True
        tmp = load_ogs5msh(filepath, **kwargs)
        if isinstance(tmp, list) and not isinstance(self, MSH):
            print(
                filepath
                + " may contains a multi-layer mesh."
                + "Try loading within the multimesh class."
            )
        elif not isinstance(tmp, list):
            tmp = [tmp]
        if "verbose" in kwargs:
            verbose = kwargs["verbose"]
        else:
            verbose = False
        if check_mesh_list(tmp, verbose=verbose):
            self._block = 0
            self._meshlist = tmp
        else:
            raise ValueError("MSH: " + filepath + ": given mesh is not valid")

    def read_file(self, path, encoding=None, verbose=False):
        """
        Load an OGS5 mesh from file.

        Parameters
        ----------
        path : str
            path to the '\*.msh' OGS5 mesh file to load
        encoding : str or None, optional
            encoding of the given file. If ``None`` is given, the system
            standard is used. Default: ``None``
        verbose : bool, optional
            Print information of the reading process. Default: True
        """
        self.load(
            path, verbose=verbose, ignore_unknown=True, encoding=encoding
        )

    def set_dict(self, mesh_dict):
        """
        Set an mesh as returned by tools methods or generators.
        Mesh will be checked for validity.

        Parameters
        ----------
        mesh_dict : dict or None, optional
            Contains one '#FEM_MSH' block of an OGS5 mesh file
            with the following information (sorted by keys):

                mesh_data : dict
                    dictionary containing information about

                    - AXISYMMETRY (bool)
                    - CROSS_SECTION (bool)
                    - PCS_TYPE (str)
                    - GEO_TYPE (str)
                    - GEO_NAME (str)
                    - LAYER (int)

                nodes : ndarray
                    Array with all node postions
                elements : dict
                    contains nodelists for elements sorted by element types
                material_id : dict
                    contains material ids for each element sorted by element types
                element_id : dict
                    contains element ids for each element sorted by element types
        """
        if check_mesh_dict(mesh_dict):
            self._dict = mesh_dict
        else:
            print("given mesh is not valid")

    def save(self, path, **kwargs):
        """
        Save the mesh to an OGS5 mesh file.
        kwargs will be forwarded to "tools.save_ogs5msh"

        Parameters
        ----------
        path : string
            path to the '\*.msh' OGS5 mesh file to save
        verbose : bool, optional
            Print information of the writing process. Default: True
        """
        # no top-comment allowed in MSH file
        if "verbose" in kwargs:
            verbose = kwargs["verbose"]
        else:
            kwargs["verbose"] = verbose = False
        if self.check(verbose=verbose):
            save_ogs5msh(
                path,
                self._meshlist,
                top_com=None,
                bot_com=self.bot_com,
                **kwargs
            )
        else:
            print("the mesh could not be saved since it is not valid")

    def import_mesh(self, filepath, **kwargs):
        """
        import an external unstructured mesh from diffrent file-formats
        kwargs will be forwarded to "tools.import_mesh"

        Parameters
        ----------
        filepath : string
            path to the mesh file to import
        file_format : str, optional
            Here you can specify the fileformat. If 'None' it will be
            determined by file extension. Default: None
        ignore_unknown : bool, optional
            Unknown data in the file will be ignored. Default: False
        import_dim : iterable of int, optional
            State which elements should be imported by dimensionality.
            Can be used to sort out unneeded elements for example from gmsh.
            Default: (1, 2, 3)

        Notes
        -----
        This routine calls the 'read' function from the meshio package
        and converts the output (see here: https://github.com/nschloe/meshio)
        If there is any "vertex" (0D element) in the element data,
        it will be removed.
        """
        tmp = import_mesh(filepath, **kwargs)
        if check_mesh_dict(tmp):
            self._meshlist = [tmp]
        else:
            raise ValueError("MSH:" + filepath + ": given mesh is not valid")

    def export_mesh(self, filepath, verbose=False, **kwargs):
        """
        export the mesh to an unstructured mesh in diffrent file-formats
        kwargs will be forwarded to "tools.export_mesh"

        Parameters
        ----------
        filepath : string
            path to the file to export
        file_format : str, optional
            Here you can specify the fileformat. If 'None' it will be
            determined by file extension. Default: None
        verbose : bool, optional
            Print information for the executed checks. Default: True
        export_material_id : bool, optional
            Here you can specify if the material_id should be exported.
            Default: True
        add_data_by_id : ndarray, optional
            Here you can specify additional element data sorted by their IDs.
            Default: None

        Notes
        -----
        This routine calls the 'write' function from the meshio package
        and converts the input (see here: https://github.com/nschloe/meshio)
        """
        if self.check(verbose=verbose):
            export_mesh(filepath, self._dict, **kwargs)
        else:
            print("the mesh could not be exported since it is not valid")

    def combine_mesh(self, ext_mesh, **kwargs):
        """
        Combine this mesh with an external mesh. The node list will be
        updated to eliminate duplicates.
        Element intersections are not checked.
        kwargs will be forwarded to "tools.combine"

        Parameters
        ----------
        ext_mesh: mesh, dict or file
            This is the mesh that should be added to the existing one.
        decimals : int, optional
            Number of decimal places to round the nodes to (default: 3).
            This will not round the output, it is just for comparison of the
            node vectors.
        fast : bool, optional
            If fast is True, the vector comparison is executed by a
            decimal comparison. If fast is False, all pairwise distances
            are calculated. Default: False
        """
        if isinstance(ext_mesh, MSH):
            tmp_mesh = ext_mesh()
        elif isinstance(ext_mesh, dict):
            tmp_mesh = ext_mesh
        else:
            try:
                tmp_mesh = load_ogs5msh(ext_mesh)
            except Exception:
                try:
                    tmp_mesh = import_mesh(ext_mesh)
                except Exception:
                    print("Could not interpret the mesh that should be added")
                    return

        if check_mesh_dict(tmp_mesh, verbose=False):
            self._dict = combine(self._dict, tmp_mesh, **kwargs)
        else:
            print("given mesh to add is not valid")

    def check(self, verbose=True):
        """
        Check if the mesh is valid in the sence, that the
        contained data is consistent.
        Checks for correct element definitions or Node duplicates
        are not carried out.

        Parameters
        ----------
        verbose : bool, optional
            Print information for the executed checks. Default: True

        Returns
        -------
        result : bool
            Validity of the given mesh.
        """
        return check_mesh_list(self._meshlist, verbose=verbose)

    def swap_axis(self, axis1="y", axis2="z"):
        """
        Swap axis of the coordinate system

        Parameters
        ----------
        axis1 : :class:`str` or :class:`int`, optional
            First selected Axis.
            Either in ["x", "y", "z"] or in [0, 1, 2]. Default: "y"
        axis2 : :class:`str` or :class:`int`, optional
            Second selected Axis.
            Either in ["x", "y", "z"] or in [0, 1, 2]. Default: "z"
        """
        axis = ["x", "y", "z"]
        if axis1 in range(3):
            axis1 = axis[axis1]
        if axis2 in range(3):
            axis2 = axis[axis2]
        if axis1 not in axis or axis2 not in axis:
            raise ValueError(
                "MSH.swap_axis: axis need to be 'x', 'y' or 'z': "
                + str(axis1)
                + ", "
                + str(axis2)
            )
        if axis1 == axis2:
            raise ValueError(
                "MSH.swap_axis: please select distict axis: "
                + str(axis1)
                + " = "
                + str(axis2)
            )
        ax1 = axis.index(axis1)
        ax2 = axis.index(axis2)
        self.NODES[:, [ax1, ax2]] = self.NODES[:, [ax2, ax1]]

    def rotate(
        self,
        angle,
        rotation_axis=(0.0, 0.0, 1.0),
        rotation_point=(0.0, 0.0, 0.0),
    ):
        """
        Rotate a given mesh around a given rotation axis with a given angle.

        Parameters
        ----------
        angle : float
            rotation angle given in radial length
        rotation_axis : array_like, optional
            Array containing the vector for ratation axis. Default: (0,0,1)
        rotation_point : array_like, optional
            Vector of the ratation base point. Default:(0,0,0)
        """
        rotate_mesh(self._dict, angle, rotation_axis, rotation_point)

    def shift(self, vector):
        """
        Shift a given mesh with a given vector.

        Parameters
        ----------
        vector : ndarray
            array containing the shifting vector
        """
        shift_mesh(self._dict, vector)

    def transform(self, xyz_func, **kwargs):
        """
        Transform a given mesh with a given function "xyz_func".
        kwargs will be forwarded to "xyz_func".

        Parameters
        ----------
        xyz_func : function
            the function transforming the points:
            ``x_new, y_new, z_new = f(x_old, y_old, z_old, **kwargs)``
        """
        transform_mesh(self._dict, xyz_func, **kwargs)

    def remove_dim(self, remove):
        """
        Remove elements by given dimensions from a mesh.

        Parameters
        ----------
        remove : iterable of int or single int
            State which elements should be removed by dimensionality (1, 2, 3).
        """
        remove_dim(self._dict, remove=remove)

    def generate(self, generator="rectangular", **kwargs):
        """
        Use a mesh-generator from the generator module

        See: :any:`ogs5py.fileclasses.msh.generator`

        Parameters
        ----------
        generator : str
            set the generator from the generator module
        **kwargs
            kwargs will be forwarded to the generator in use

        Notes
        -----
        .. currentmodule:: ogs5py.fileclasses.msh.generator

        The following generators are available:

        .. autosummary::
           rectangular
           radial
           grid_adapter2D
           grid_adapter3D
           block_adapter3D
           generate_gmsh
        """
        self._dict = getattr(gen, generator)(**kwargs)

    def show(self, show_element_id=True):
        """
        Display the mesh colored by its material ID.

        Parameters
        ----------
        show_element_id : bool, optional
            Here you can specify if the mesh should be colored by material_id.
            Default: True

        Notes
        -----
        This routine needs "mayavi" to display the mesh.
        (see here: https://github.com/enthought/mayavi)
        """
        from ogs5py.fileclasses.msh.viewer import show_mesh

        show_mesh(self._dict, show_element_id=show_element_id)

    #######################
    ### Special methods
    #######################
    def __call__(self):
        return dcp(self._dict)

    def __repr__(self):
        out = "#FEM_MSH\n"
        if self.AXISYMMETRY:
            out += " $AXISYMMETRY\n"
        if self.CROSS_SECTION:
            out += " $CROSS_SECTION\n"
        if self.PCS_TYPE is not None:
            out += " $PCS_TYPE\n"
            out += "  " + self.PCS_TYPE + "\n"
        if self.GEO_NAME is not None:
            out += " $GEO_NAME\n"
            out += "  " + self.GEO_NAME + "\n"
        if self.GEO_TYPE is not None:
            out += " $GEO_TYPE\n"
            out += "  " + self.GEO_TYPE + " " + self.GEO_NAME + "\n"
        if self.LAYER is not None:
            out += " $LAYER\n"
            out += "  " + str(self.LAYER) + "\n"
        out += " $NODES\n"
        if self.NODES is None:
            out += "  None\n"
        else:
            out += "  " + str(self.NODES.shape[0]) + "\n"
            out += "   ...\n"
        out += " $ELEMENTS\n"
        if self.ELEMENTS is None:
            out += "  None\n"
        else:
            elem_no = 0
            for elem in self.ELEMENTS:
                elem_no += self.ELEMENTS[elem].shape[0]
            out += "  " + str(elem_no) + "\n"
            out += "   ...\n"
        out += "#STOP\n"
        return out


class MSH(MSHsgl):
    """
    Class for a multi layer mesh file that contains multiple '#FEM_MSH' Blocks

    Parameters
    ----------
    mesh_list : list of dict or None, optional
        each dictionary contains one '#FEM_MSH' block of the mesh file with
        with the following information (sorted by keys):

            mesh_data : dict
                dictionary containing information about

                - AXISYMMETRY (bool)
                - CROSS_SECTION (bool)
                - PCS_TYPE (str)
                - GEO_TYPE (str)
                - GEO_NAME (str)
                - LAYER (int)

            nodes : ndarray
                Array with all node postions
            elements : dict
                contains nodelists for elements sorted by element types
            material_id : dict
                contains material ids for each element sorted by element types
            element_id : dict
                contains element ids for each element sorted by element types

    task_root : str, optional
        Path to the destiny model folder.
        Default: cwd+"ogs5model"
    task_id : str, optional
        Name for the ogs task.
        Default: "model"
    """

    def __init__(self, mesh_list=None, **OGS_Config):
        super(MSH, self).__init__(None, **OGS_Config)

        if mesh_list is None:
            self.__meshlist = [EMPTY_MSH]
        else:
            self.__meshlist = mesh_list

    # meshlist (override the property of MSHsgl) #    @property
    @MSHsgl._meshlist.getter
    def _meshlist(self):
        return self.__meshlist

    @_meshlist.setter
    def _meshlist(self, value):
        self.__meshlist = value
        if len(self.__meshlist) >= self._block:
            self._block = 0

    @_meshlist.deleter
    def _meshlist(self):
        self.__meshlist = [EMPTY_MSH]
        self._block = 0

    # override the _dict property
    @MSHsgl._dict.getter
    def _dict(self):
        return self.__meshlist[self.block]

    @_dict.setter
    def _dict(self, value):
        self.__meshlist[self.block] = value

    @property
    def block_no(self):
        """:class:`int`: The number of blocks in the file."""
        return len(self.__meshlist)

    # select the block to be edited
    @property
    def block(self):
        """:class:`int`: The actual block to access in the file."""
        return self._block

    @block.setter
    def block(self, value):
        value = int(value)
        if 0 <= value < len(self.__meshlist):
            self._block = value
        if -len(self.__meshlist) <= value < 0:
            self._block = len(self.__meshlist) - value
        if value == len(self.__meshlist):
            self._block = value
            self.__meshlist.append(EMPTY_MSH)

    @block.deleter
    def block(self):
        self._block = 0

    def __repr__(self):
        out = ""
        old_block = self.block
        for i in range(len(self._meshlist)):
            self.block = i
            out += "#FEM_MSH\n"
            if self.AXISYMMETRY:
                out += " $AXISYMMETRY\n"
            if self.CROSS_SECTION:
                out += " $CROSS_SECTION\n"
            if self.PCS_TYPE is not None:
                out += " $PCS_TYPE\n"
                out += "  " + self.PCS_TYPE + "\n"
            if self.GEO_NAME is not None:
                out += " $GEO_NAME\n"
                out += "  " + self.GEO_NAME + "\n"
            if self.GEO_TYPE is not None:
                out += " $GEO_TYPE\n"
                out += "  " + self.GEO_TYPE + " " + self.GEO_NAME + "\n"
            if self.LAYER is not None:
                out += " $LAYER\n"
                out += "  " + str(self.LAYER) + "\n"
            out += " $NODES\n"
            if self.NODES is None:
                out += "  None\n"
            else:
                out += "  " + str(self.NODES.shape[0]) + "\n"
                out += "   ...\n"
            out += " $ELEMENTS\n"
            if self.ELEMENTS is None:
                out += "  None\n"
            else:
                out += "  " + str(self.ELEMENT_NO) + "\n"
                out += "   ...\n"
        if self._meshlist:
            out += "#STOP\n"
        self.block = old_block
        return out

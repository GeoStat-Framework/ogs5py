# -*- coding: utf-8 -*-
"""
core module for the ogs5py GLI file.
Containing the classes for the OGS5 GLI files.
"""

from __future__ import division, print_function, absolute_import
from copy import deepcopy as dcp
import os
import numpy as np

# import ogs5py.fileclasses.gli.generator as gen
from ogs5py.tools.types import STRTYPE, EMPTY_GLI
from ogs5py.fileclasses.gli.checker import (
    check_gli_dict,
    check_polyline,
    check_surface,
    check_volume,
)
from ogs5py.fileclasses.gli.tools import load_ogs5gli, save_ogs5gli
from ogs5py.tools.tools import (
    is_str_array,
    rotate_points,
    shift_points,
    unique_rows,
    replace,
)
from ogs5py.fileclasses.base import File

# current working directory
CWD = os.getcwd()


class GLI(File):
    """
    Class for the ogs GEOMETRY file.

    Parameters
    ----------
    gli_dict : :class:`dict` or :class:`None`, optional
        dictionary containing the gli file
        Includes the following information (sorted by keys):

            points : ndarray
                Array with all point postions
            point_names : ndarray (of strings)
                Array with all point names
            point_md : ndarray
                Array with all Material-densities at the points
                if point_md should be undefined it takes the value -np.inf
            polylines : list of dict
                each containing information about

                - ``ID`` (int or None)
                - ``NAME`` (str)
                - ``POINTS`` (ndarray)
                - ``EPSILON`` (float or None)
                - ``TYPE`` (int or None)
                - ``MAT_GROUP`` (int or None)
                - ``POINT_VECTOR`` (str or None)

            surfaces : list of dict
                each containing information about

                - ``ID`` (int or None)
                - ``NAME`` (str)
                - ``POLYLINES`` (list of str)
                - ``EPSILON`` (float or None)
                - ``TYPE`` (int or None)
                - ``MAT_GROUP`` (int or None)
                - ``TIN`` (str or None)

            volumes : list of dict
                each containing information about

                - ``NAME`` (str)
                - ``SURFACES`` (list of str)
                - ``TYPE`` (int or None)
                - ``MAT_GROUP`` (int or None)
                - ``LAYER`` (int or None)

        Default: :class:`None`
    task_root : :class:`str`, optional
        Path to the destiny model folder.
        Default: cwd+"ogs5model"
    task_id : :class:`str`, optional
        Name for the ogs task.
        Default: "model"
    """

    def __init__(self, gli_dict=None, **OGS_Config):
        super(GLI, self).__init__(**OGS_Config)
        self.file_ext = ".gli"
        self.force_writing = True

        if gli_dict is None:
            self.__dict = dcp(EMPTY_GLI)
        elif check_gli_dict(gli_dict):
            self.__dict = gli_dict
        else:
            print("given gli_dict is not valid.. will set default")
            self.__dict = dcp(EMPTY_GLI)

    #        self.mainkw = [""]

    # Pretend that there is a main keyword in the standard BASE-FORMAT
    @property
    def is_empty(self):
        """:class:`bool`: State if the GLI File is empty"""
        return self.POINTS is None

    #######################
    # POINTS
    #######################
    @property
    def POINTS(self):
        """ndarray: POINTS (n,3) of the gli, defined by xyz-coordinates.
        """
        return self.__dict["points"]

    @POINTS.setter
    def POINTS(self, value):
        # del self.POINTS
        self.__dict["points"] = np.array(value, dtype=float)

    @POINTS.deleter
    def POINTS(self):
        self.__dict["points"] = None
        del self.POINT_NAMES
        del self.POINT_MD
        del self.POLYLINES
        del self.SURFACES
        del self.VOLUMES

    #######################
    # POINT_NO
    #######################
    @property
    def POINT_NO(self):
        """int: number of POINTS of the gli."""
        if self.POINTS is None:
            return 0
        return self.POINTS.shape[0]

    #######################
    # POINT_NAMES
    #######################
    @property
    def POINT_NAMES(self):
        """ndarray: names of POINTS of the gli."""
        return self.__dict["point_names"]

    @POINT_NAMES.setter
    def POINT_NAMES(self, value):
        self.__dict["point_names"] = np.array(value, dtype=object)

    @POINT_NAMES.deleter
    def POINT_NAMES(self):
        if self.POINTS is not None:
            self.__dict["point_names"] = np.array(
                self.POINT_NO * [""], dtype=object
            )
        else:
            self.__dict["point_names"] = None

    #######################
    # POINT_MD
    #######################
    @property
    def POINT_MD(self):
        """ndarray: material density values of POINTS of the gli."""
        return self.__dict["point_md"]

    @POINT_MD.setter
    def POINT_MD(self, value):
        self.__dict["point_md"] = np.array(value, dtype=float)

    @POINT_MD.deleter
    def POINT_MD(self):
        if self.POINTS is not None:
            self.__dict["point_md"] = -np.inf * np.ones(
                self.POINT_NO, dtype=float
            )
        else:
            self.__dict["point_md"] = None

    #######################
    # POLYLINES
    #######################
    @property
    def POLYLINES(self):
        """list of dict: POLYLINES of the gli."""
        return self.__dict["polylines"]

    #######################
    # POLYLINE_NAMES
    #######################
    @property
    def POLYLINE_NAMES(self):
        """list of str: names of POLYLINES of the gli."""
        ply_names = []
        for ply in self.POLYLINES:
            ply_names.append(ply["NAME"])
        return ply_names

    #######################
    # POLYLINE_NO
    #######################
    @property
    def POLYLINE_NO(self):
        """int: number of POLYLINES of the gli."""
        return len(self.POLYLINES)

    #######################
    # SURFACES
    #######################
    @property
    def SURFACES(self):
        """list of dict: SURFACES of the gli."""
        return self.__dict["surfaces"]

    #######################
    # SURFACE_NAMES
    #######################
    @property
    def SURFACE_NAMES(self):
        """list of str: names of SURFACES of the gli."""
        srf_names = []
        for srf in self.SURFACES:
            srf_names.append(srf["NAME"])
        return srf_names

    #######################
    # SURFACE_NO
    #######################
    @property
    def SURFACE_NO(self):
        """int: number of SURFACES of the gli."""
        return len(self.SURFACES)

    #######################
    # VOLUMES
    #######################
    @property
    def VOLUMES(self):
        """list of dict: VOLUMES of the gli."""
        return self.__dict["volumes"]

    #######################
    # VOLUME_NAMES
    #######################
    @property
    def VOLUME_NAMES(self):
        """list of str: names of VOLUMES of the gli."""
        vol_names = []
        for vol in self.VOLUMES:
            vol_names.append(vol["NAME"])
        return vol_names

    #######################
    # VOLUME_NO
    #######################
    @property
    def VOLUME_NO(self):
        """int: number of VOLUMES of the gli."""
        return len(self.VOLUMES)

    #######################
    # Class methods
    #######################
    def reset(self):
        """
        Delete every content.
        """
        self.__dict = EMPTY_GLI

    def load(self, filepath, verbose=False, encoding=None, **kwargs):
        """
        Load an OGS5 gli from file.
        kwargs will be forwarded to "tools.load_ogs5gli"

        Parameters
        ----------
        filepath : string
            path to the '\*.gli' OGS5 gli file to load
        verbose : bool, optional
            Print information of the reading process. Default: True
        """
        tmp = load_ogs5gli(
            filepath, verbose=verbose, encoding=encoding, **kwargs
        )
        if check_gli_dict(tmp, verbose=verbose):
            self.__dict = tmp
        else:
            raise ValueError(
                "GLI.load: " + filepath + ": given gli is not valid"
            )

    def read_file(self, path, encoding=None, verbose=False):
        """
        Load an OGS5 gli from file.

        Parameters
        ----------
        path : string
            path to the '\*.gli' OGS5 gli file to load
        encoding : str or None, optional
            encoding of the given file. If ``None`` is given, the system
            standard is used. Default: ``None``
        verbose : bool, optional
            Print information of the reading process. Default: False
        """
        self.load(path, verbose=verbose, encoding=encoding)

    def set_dict(self, gli_dict):
        """
        Set a gli dict as returned by tools methods or generators.
        Gli will be checked for validity.

        Parameters
        ----------
        gli_dict : :class:`dict`
            dictionary containing the gli file
            Includes the following information (sorted by keys):

                points : ndarray
                    Array with all point postions
                point_names : ndarray (of strings)
                    Array with all point names
                point_md : ndarray
                    Array with all Material-densities at the points
                    if point_md should be undefined it takes the value -np.inf
                polylines : list of dict
                    each containing information about

                    - ``ID`` (int or None)
                    - ``NAME`` (str)
                    - ``POINTS`` (ndarray)
                    - ``EPSILON`` (float or None)
                    - ``TYPE`` (int or None)
                    - ``MAT_GROUP`` (int or None)
                    - ``POINT_VECTOR`` (str or None)

                surfaces : list of dict
                    each containing information about

                    - ``ID`` (int or None)
                    - ``NAME`` (str)
                    - ``POLYLINES`` (list of str)
                    - ``EPSILON`` (float or None)
                    - ``TYPE`` (int or None)
                    - ``MAT_GROUP`` (int or None)
                    - ``TIN`` (str or None)

                volumes : list of dict
                    each containing information about

                    - ``NAME`` (str)
                    - ``SURFACES`` (list of str)
                    - ``TYPE`` (int or None)
                    - ``MAT_GROUP`` (int or None)
                    - ``LAYER`` (int or None)
        """
        if check_gli_dict(gli_dict):
            self.__dict = gli_dict
        else:
            print("given gli_dict is not valid")

    def save(self, path, **kwargs):
        """
        Save the gli to an OGS5 gli file.
        kwargs will be forwarded to "tools.save_ogs5gli"

        Parameters
        ----------
        path : string
            path to the '\*.gli' OGS5 gli file to save
        verbose : bool, optional
            Print information of the writing process. Default: True
        """
        if "verbose" in kwargs:
            verbose = kwargs["verbose"]
        else:
            kwargs["verbose"] = verbose = False
        if self.check(verbose=verbose):
            save_ogs5gli(
                path,
                self.__dict,
                top_com=self.top_com,
                bot_com=self.bot_com,
                **kwargs
            )
        else:
            print("the mesh could not be saved since it is not valid")

    def check(self, verbose=True):
        """
        Check if the gli is valid in the sence, that the
        contained data is consistent.

        Parameters
        ----------
        verbose : bool, optional
            Print information for the executed checks. Default: True

        Returns
        -------
        result : bool
            Validity of the given gli.
        """
        return check_gli_dict(self.__dict, verbose=verbose)

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
                "GLI.swap_axis: axis need to be 'x', 'y' or 'z': "
                + str(axis1)
                + ", "
                + str(axis2)
            )
        if axis1 == axis2:
            raise ValueError(
                "GLI.swap_axis: please select distict axis: "
                + str(axis1)
                + " = "
                + str(axis2)
            )
        ax1 = axis.index(axis1)
        ax2 = axis.index(axis2)
        self.POINTS[:, [ax1, ax2]] = self.POINTS[:, [ax2, ax1]]

    def rotate(
        self,
        angle,
        rotation_axis=(0.0, 0.0, 1.0),
        rotation_point=(0.0, 0.0, 0.0),
    ):
        """
        Rotate points around a given rotation point and axis
        with a given angle.

        Parameters
        ----------
        angle : float
            rotation angle given in radial length
        rotation_axis : array_like, optional
            Array containing the vector for ratation axis. Default: (0,0,1)
        rotation_point : array_like, optional
            Vector of the ratation base point. Default:(0,0,0)
        """
        self.POINTS = rotate_points(
            self.POINTS, angle, rotation_axis, rotation_point
        )

    def shift(self, vector):
        """
        Shift points with a given vector.

        Parameters
        ----------
        vector : ndarray
            array containing the shifting vector
        """
        self.POINTS = shift_points(self.POINTS, vector)

    def generate(self, generator="rectangular", **kwargs):
        """
        Use a gli-generator from the generator module

        See: :any:`ogs5py.fileclasses.gli.generator`

        Parameters
        ----------
        generator : str
            set the generator from the generator module
        **kwargs
            kwargs will be forwarded to the generator in use
        """
        from ogs5py.fileclasses.gli import generator as gen

        self.__dict = getattr(gen, generator)(**kwargs)

    def add_points(self, points, names=None, md=None, decimals=4):
        """
        Add a list of points (ndarray with shape (n,3)) and keep the
        pointlist unique. If a named point is added, that was already present,
        it will be renamed with the new name. Same for md.
        The pointlists of the polylines will be updated.

        Parameters
        ----------
        points : ndarray
            Array with new points.
        names : ndarray of str or None, optional
            array containing the names.
            If None, all new points are unnamed.
            Default: None
        md : ndarray of float or None, optional
            array containing the material densitiy.
            If None, all new points will have unspecified md.
            Default: None
        decimals : int, optional
            Number of decimal places to round the added points to (default: 4).
            If decimals is negative, it specifies the number of positions
            to the left of the decimal point.
            This will not round the new points, it's just for comparison of the
            already present points to guarante uniqueness.

        Returns
        -------
        new_pos : ndarray
            array with the IDs of the added points in the pointlist of the gli.
        """
        # check if given points are unique
        points = np.array(points, dtype=float, ndmin=2)
        if names is not None:
            names = np.array(names, dtype=object, ndmin=1)
            if points.shape[0] != names.shape[0]:
                print("gli.add_points: Given names are not valid!")
                return np.zeros(0)
        if md is not None:
            md = np.array(md, dtype=float, ndmin=1)
            if points.shape[0] != md.shape[0]:
                print("gli.add_points: Given MDs are not valid!")
                return np.zeros(0)
        if points.shape[1] != 3:
            print("gli.add_points: Given points are not valid!")
            return np.zeros(0)
        check_points, __, __ = unique_rows(points, decimals=decimals)
        if check_points.shape[0] != points.shape[0]:
            print("gli.add_points: Given points are not unique!")
            return np.zeros(0)
        # workaround, if Points are None
        if self.POINT_NO == 0:
            self.POINTS = np.empty((0, 3), dtype=float)
            self.POINT_NAMES = np.empty(0, dtype=object)
            self.POINT_MD = np.empty(0, dtype=float)
        new_points = np.vstack((self.POINTS, points))
        new_points, __, ixr = unique_rows(new_points, decimals=decimals)
        old_pos = ixr[: self.POINT_NO]
        new_pos = ixr[self.POINT_NO :]
        # set the new names
        new_names = np.array(new_points.shape[0] * [""], dtype=object)
        new_names[old_pos] = self.POINT_NAMES
        if names is not None:
            new_names[new_pos] = names
        # set the new MDs
        new_md = -np.inf * np.ones(new_points.shape[0], dtype=float)
        new_md[old_pos] = self.POINT_MD
        if md is not None:
            new_md[new_pos] = md
        # reset the point IDs within the polylines
        for ply_i in range(self.POLYLINE_NO):
            self.__dict["polylines"][ply_i]["POINTS"] = replace(
                self.__dict["polylines"][ply_i]["POINTS"],
                np.arange(self.POINT_NO),
                old_pos,
            )
        # set the new points
        self.POINTS = new_points
        self.POINT_NAMES = new_names
        self.POINT_MD = new_md
        # return the new positions of the added points
        return new_pos

    def add_polyline(
        self,
        name,
        points,
        ply_id=None,
        epsilon=None,
        ply_type=None,
        mat_group=None,
        point_vector=None,
        closed=False,
        decimals=4,
    ):
        """
        Add a polyline to the gli.

        Parameters
        ----------
        points : ndarray
            Array with new points. Either of shape (n,3) to add new points
            by their coordinates or a list of points IDs refering to existing
            points.
        name : str
            name of the new polyline
        points : ndarray
            Array with the points. Either array of point IDs
            or new coordinates.
        ply_id : int or None, optional
            Default: None
        epsilon : float or None, optional
            Default: None
        ply_type : int or None, optional
            Default: None
        mat_group : int or None, optional
            Default: None
        point_vector : str or None, optional
            Default: None
        closed : bool, optional
            If the polyline shall be closed, the first point will be added
            as last point again. Default: False
        decimals : int, optional
            Number of decimal places to round the added points to (default: 4).
            If decimals is negative, it specifies the number of positions
            to the left of the decimal point.
            This will not round the new points, it's just for comparison of the
            already present points to guarante uniqueness.
        """
        points = np.asanyarray(points)
        name = str(name)
        safe_dict = self()
        if name in self.POLYLINE_NAMES:
            print("gli.add_polyline: Polyline-name already present!")
            return
        # add by id
        if (
            np.issubdtype(points.dtype, np.integer)
            and points.ndim == 1
            and points.shape[0] >= 2
            and np.min(points) >= 0
            and np.max(points) < self.POINT_NO
        ):
            if closed:
                points = np.hstack((points, points[0]))
            new_ply = {
                "NAME": name,
                "POINTS": points,
                "ID": ply_id,
                "EPSILON": epsilon,
                "TYPE": ply_type,
                "MAT_GROUP": mat_group,
                "POINT_VECTOR": point_vector,
            }
        # add by name
        elif (
            is_str_array(points)
            and points.ndim == 1
            and points.shape[0] >= 2
            and all([str(pnt) in self.POINT_NAMES for pnt in points])
        ):
            if closed:
                points = np.hstack((points, points[0]))
            # get IDs from the given names
            # see: https://stackoverflow.com/a/32191125/6696397
            # after the check, if points are IDs...
            points = np.array(
                [
                    np.where(self.POINT_NAMES == str(pnt))[0][0]
                    for pnt in points
                ],
                dtype=int,
            )
            new_ply = {
                "NAME": name,
                "POINTS": points,
                "ID": ply_id,
                "EPSILON": epsilon,
                "TYPE": ply_type,
                "MAT_GROUP": mat_group,
                "POINT_VECTOR": point_vector,
            }
        # add by coordinates
        elif (
            np.issubdtype(points.dtype, np.floating)
            and points.ndim == 2
            and points.shape[0] >= 2
            and points.shape[1] == 3
        ):
            if closed:
                points = np.vstack((points, points[0]))
            unique_pnt, __, ixr = unique_rows(points, decimals=decimals)
            new_pos = self.add_points(unique_pnt, decimals=decimals)
            new_points = replace(ixr, np.arange(unique_pnt.shape[0]), new_pos)
            new_ply = {
                "NAME": name,
                "POINTS": new_points,
                "ID": ply_id,
                "EPSILON": epsilon,
                "TYPE": ply_type,
                "MAT_GROUP": mat_group,
                "POINT_VECTOR": point_vector,
            }
        else:
            print("gli.add_polyline: Polyline-points not valid!")
            return
        # add the new polyline
        self.__dict["polylines"].append(new_ply)
        if not check_polyline(new_ply, self.POINT_NO, verbose=False):
            print("gli.add_polyline: Polyline not valid!")
            self.__dict = safe_dict

    def add_surface(
        self,
        name,
        polylines,
        srf_id=None,
        epsilon=None,
        srf_type=0,
        mat_group=None,
        tin=None,
    ):
        """
        Add a new surface.

        Parameters
        ----------
        name : str
            name of the new surface
        polylines : list of str
            List of the surface-defining polyline-names
        srf_id : int or None, optional
            Default: None
        epsilon : float or None, optional
            Default: None
        srf_type : int or None, optional
            Default: None
        mat_group : int or None, optional
            Default: None
        tin : str or None, optional
            Default: None
        """
        name = str(name)
        if name in self.SURFACE_NAMES:
            print("gli.add_surface: Surface-name already present!")
            return
        new_srf = {
            "NAME": name,
            "POLYLINES": polylines,
            "ID": srf_id,
            "EPSILON": epsilon,
            "TYPE": srf_type,
            "MAT_GROUP": mat_group,
            "TIN": tin,
        }
        if not check_surface(new_srf, self.POLYLINE_NAMES, verbose=False):
            print("gli.add_surface: Surface not valid!")
        else:
            self.__dict["surfaces"].append(new_srf)

    def add_volume(
        self, name, surfaces, vol_type=None, mat_group=None, layer=None
    ):
        """
        Add a new volume.

        Parameters
        ----------
        name : str
            name of the new surface
        surfaces : list of str
            List of the volume-defining surface-names
        vol_type : int or None, optional
            Default: None
        mat_group : int or None, optional
            Default: None
        layer : int or None, optional
            Default: None
        """
        name = str(name)
        if name in self.VOLUME_NAMES:
            print("gli.add_volume: Volume-name already present!")
            return
        new_vol = {
            "NAME": name,
            "SURFACES": surfaces,
            "TYPE": vol_type,
            "MAT_GROUP": mat_group,
            "LAYER": layer,
        }
        if not check_volume(new_vol, self.SURFACE_NAMES, verbose=False):
            print("gli.add_volume: Volume not valid!")
        else:
            self.__dict["volumes"].append(new_vol)

    def remove_point(self, id_or_name):
        """
        Remove a point by its name or ID. If Points are removed, that define
        polylines, they will be removed. Same for surfaces and volumes.

        Parameters
        ----------
        id_or_name : int or str or list of int or list of str
            Points to be removed. Unknown names or IDs are ignored.
        """
        if not isinstance(id_or_name, (list, tuple, set)):
            id_or_name = [id_or_name]

        index_list = []
        for pnt in id_or_name:
            index = -1
            if isinstance(pnt, STRTYPE) and pnt in self.POINT_NAMES:
                index = list(self.POINT_NAMES).index(pnt)
            else:
                try:
                    pnt = int(pnt)
                except ValueError:
                    continue
                if 0 <= pnt < self.POINT_NO:
                    index = pnt
            if index == -1:
                continue
            if index not in index_list:
                index_list.append(index)

        ply_remove = []
        for ply in self.POLYLINES:
            if any([idx in ply["POINTS"] for idx in index_list]):
                ply_remove.append(ply["NAME"])
        self.remove_polyline(ply_remove)

        old_ids = np.delete(np.arange(self.POINT_NO), index_list, 0)
        new_ids = np.arange(len(old_ids))

        for ply in self.POLYLINES:
            ply["POINTS"] = replace(ply["POINTS"], old_ids, new_ids)

        self.POINTS = np.delete(self.POINTS, index_list, 0)
        self.POINT_NAMES = np.delete(self.POINT_NAMES, index_list, 0)
        self.POINT_MD = np.delete(self.POINT_MD, index_list, 0)

    def remove_polyline(self, names):
        """
        Remove a polyline by its name. If Polylines are removed, that define
        surfaces, they will be removed. Same for volumes.

        Parameters
        ----------
        names : str or list of str
            Polylines to be removed. Unknown names are ignored.
        """
        if not isinstance(names, (list, tuple, set)):
            names = [names]
        for ply_name in names:
            if ply_name not in self.POLYLINE_NAMES:
                continue
            srf_remove = []
            for srf in self.SURFACES:
                if ply_name in srf["POLYLINES"]:
                    srf_remove.append(srf["NAME"])
            self.remove_surface(srf_remove)

            del self.POLYLINES[self.POLYLINE_NAMES.index(ply_name)]

    def remove_surface(self, names):
        """
        Remove a surface by its name. If Surfaces are removed, that define
        Volumes, they will be removed.

        Parameters
        ----------
        names : str or list of str
            Surfaces to be removed. Unknown names are ignored.
        """
        if not isinstance(names, (list, tuple, set)):
            names = [names]
        for srf_name in names:
            if srf_name not in self.SURFACE_NAMES:
                continue
            vol_remove = []
            for vol in self.VOLUMES:
                if srf_name in vol["SURFACES"]:
                    vol_remove.append(vol["NAME"])
            self.remove_volume(vol_remove)

            del self.SURFACES[self.SURFACE_NAMES.index(srf_name)]

    def remove_volume(self, names):
        """
        Remove a volume by its name.

        Parameters
        ----------
        names : str or list of str
            Volumes to be removed. Unknown names are ignored.
        """
        if not isinstance(names, (list, tuple, set)):
            names = [names]
        for vol_name in names:
            if vol_name not in self.VOLUME_NAMES:
                continue
            del self.VOLUMES[self.VOLUME_NAMES.index(vol_name)]

    def pnt_coord(self, pnt_name=None, pnt_id=None):
        """
        Get Point coordinates either by name or ID.

        Parameters
        ----------
        pnt_name : str
            Point name.
        pnt_id : int
            Point ID.
        """
        # standard output is None, if pnt_name not present,
        # pnt_id out of range or both are given (ununique)
        out = None
        # search by pnt_name
        if pnt_name is not None and pnt_id is None:
            # check if pnt_name is present
            if pnt_name in self.POINT_NAMES:
                # if pnt_names have duplicates, first occurrence is returend
                out = self.POINTS[np.where(self.POINT_NAMES == pnt_name)[0][0]]
        # serach by pnt_id
        elif pnt_name is None and pnt_id is not None:
            # check if pnt_id is in range
            if pnt_id in range(self.POINT_NO):
                out = self.POINTS[pnt_id]
        return out

    #######################
    # Special methods
    #######################
    def __call__(self):
        """
        Return a copy of the underlying dictionary of the gli.

        Returns
        -------
        Mesh : dict
            dictionary representation of the mesh
        """
        return dcp(self.__dict)


class GLIext(File):
    """
    Class for an external definition for the ogs GEOMETRY file.

    Parameters
    ----------
    typ : :class:`str`, optional
        Type of the extermal geometry definition. Either ``TIN`` for a
        triangulated surface or ``POINT_VECTOR`` for a polyline.
        Default: ``"TIN"``
    data : :any:`numpy.ndarray`, optional
        Data for the external geometry definition.
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
        typ="TIN",
        data=None,
        file_name=None,
        file_ext=None,
        task_root=os.path.join(CWD, "ogs5model"),
        task_id="model",
    ):
        super(GLIext, self).__init__(task_root, task_id)

        if typ not in ["TIN", "POINT_VECTOR"]:
            raise ValueError("typ needs to be either 'TIN' or 'POINT_VECTOR'")
        self.typ = typ
        if file_name is None:
            file_name = task_id
        self.file_name = file_name
        if file_ext is None:
            if typ == "TIN":
                file_ext = ".tin"
            else:
                file_ext = ".ply"
        self.file_ext = file_ext
        if data:
            self.data = np.array(data)
        else:
            if self.typ == "TIN":
                self.data = np.zeros((0, 10))
            else:
                self.data = np.zeros((0, 3))
        if not self.check(False):
            raise ValueError("Gli external: data not valid")

    @property
    def is_empty(self):
        """state if the OGS file is empty"""
        return self.data.shape[0] == 0

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
        if self.data.ndim == 2:
            if self.typ not in ["TIN", "POINT_VECTOR"]:
                print("Gli external: Wrong typ given")
                return False
            elif self.typ == "TIN" and self.data.shape[1] != 10:
                print(
                    "Gli external: For 'TIN' the data must contain "
                    + "id + 9 Values per line"
                )
                return False
            elif self.typ == "POINT_VECTOR" and self.data.shape[1] != 3:
                print(
                    "Gli external: For 'POINT_VECTOR' the data must "
                    + "contain 3 Values per line"
                )
                return False
        else:
            if verbose:
                print("Gli external: data dimension is not 2")
                return False
        return True

    def save(self, path):
        """
        Save the actual GLI external file in the given path.

        Parameters
        ----------
        path : str
            path to where to file should be saved
        """
        np.savetxt(path, self.data)

    def read_file(self, path, **kwargs):
        """
        Read a given GLI_EXT input file.

        Parameters
        ----------
        path : str
            path to the file
        """
        if "verbose" in kwargs:
            verbose = kwargs["verbose"]
        else:
            verbose = False
        # read data
        data = np.loadtxt(path, ndmin=2)
        if data.shape[1] == 10:
            self.typ = "TIN"
            self.data = data
        elif data.shape[1] == 3:
            self.typ = "POINT_VECTOR"
            self.data = data
        elif verbose:
            print("Gli external: File data not valid")

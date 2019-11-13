# -*- coding: utf-8 -*-
"""ogs5py: a python API for OpenGeoSys5"""

import os
import codecs
import re

from setuptools import setup, find_packages


# find __version__ ############################################################


def read(*parts):
    """Read file data."""
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    """Find version without importing module."""
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


###############################################################################


VERSION = find_version("ogs5py", "_version.py")
DOCLINE = __doc__.split("\n")[0]
README = open("README.md").read()
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Intended Audience :: End Users/Desktop",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: MacOS",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
    "Operating System :: Unix",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Topic :: Scientific/Engineering",
    "Topic :: Software Development",
    "Topic :: Utilities",
]

setup(
    name="ogs5py",
    version=VERSION,
    maintainer="Sebastian Mueller",
    maintainer_email="sebastian.mueller@ufz.de",
    description=DOCLINE,
    long_description=README,
    long_description_content_type="text/markdown",
    author="Sebastian Mueller, Falk Hesse",
    author_email="info@geostat-framework.org",
    url="https://github.com/GeoStat-Framework/ogs5py",
    license="MIT",
    classifiers=CLASSIFIERS,
    platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
    include_package_data=True,
    install_requires=[
        "numpy>=1.13.0",
        "pandas>=0.23.0",  # read-routines and formatting
        "whichcraft",  # search for ogs
        "meshio",  # import/export external meshes
        "lxml",  # meshio vtu support
        "vtk",  # for the readers
        "pexpect",  # handle command calls
    ],
    extras_require={
        # "reader": ["vtk"],  # optional for reading output
        "gmsh": ["pygmsh"],  # optional for creating gmesh based meshes
        "show": ["mayavi"],  # optional to view a mesh
        "all": ["pygmsh", "mayavi"],  # everything
    },
    packages=find_packages(exclude=["tests*", "docs*"]),
)

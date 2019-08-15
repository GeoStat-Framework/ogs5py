# -*- coding: utf-8 -*-
"""
Downloader for ogs5.

.. currentmodule:: ogs5py.tools.download

Downloader
^^^^^^^^^^

A downloading routine to get the OSG5 executable.

.. autosummary::
   download_ogs

----
"""
import os
import shutil
import tarfile
import zipfile

try:  # PY3
    from urllib.request import urlretrieve
except ImportError:  # PY2
    from urllib import urlretrieve
import tempfile
import platform


# TemporaryDirectory not avialable in python2
class _TemporaryDirectory(object):
    def __enter__(self):
        self.dir_name = tempfile.mkdtemp()
        return self.dir_name

    def __exit__(self, exc_type, exc_value, traceback):
        shutil.rmtree(self.dir_name)


TemporaryDirectory = getattr(
    tempfile, "TemporaryDirectory", _TemporaryDirectory
)


URLS = {
    "5.7": {
        "Linux": (
            "https://ogsstorage.blob.core.windows.net/"
            + "binaries/ogs5/"
            + "ogs-5.7.0-Linux-2.6.32-573.8.1.el6.x86_64-x64.tar.gz"
        ),
        "Windows": (
            "https://ogsstorage.blob.core.windows.net/"
            + "binaries/ogs5/ogs-5.7.0-Windows-6.1.7601-x64.zip"
        ),
        "Darwin": (
            "https://ogsstorage.blob.core.windows.net/"
            + "binaries/ogs5/ogs-5.7.0-Darwin-15.2.0-x64.tar.gz"
        ),
    },
    "5.8": {
        "Linux": (
            "https://ogsstorage.blob.core.windows.net/"
            + "binaries/ogs5/"
            + "ogs-5.8-Linux-2.6.32-754.3.5.el6.x86_64-x64.tar.gz"
        ),
        "Windows": (
            "https://ogsstorage.blob.core.windows.net/"
            + "binaries/ogs5/ogs-5.8-Windows-x64.zip"
        ),
    },
}


def download_ogs(version="5.7", system=None, path=None, name=None):
    """
    Download the OGS5 executable.

    Parameters
    ----------
    version : :class:`str`, optional
        Version to download (5.7 or 5.8). Default: "5.7"
    system : :class:`str`, optional
        Target system (Linux, Windows, Darwin). Default: platform.system()
    path : :class:`str`, optional
        Destination path. Default: os.getcwd()
    name : :class:`str`, optional
        Destination file name. Default "ogs[.exe]"

    Notes
    -----
    There is no executable for "5.8" and "Darwin".

    Taken from : https://www.opengeosys.org/ogs-5/
    """
    system = platform.system() if system is None else system
    path = os.getcwd() if path is None else path
    path = os.path.abspath(path)
    if not os.path.exists(path):
        os.makedirs(path)
    ogs_url = URLS[version][system]
    ext = ".tar.gz" if ogs_url.endswith(".tar.gz") else ".zip"
    if name is None:
        name = "ogs.exe" if system == "Windows" else "ogs"

    with TemporaryDirectory() as tmpdirname:
        data_filename = os.path.join(tmpdirname, "data" + ext)
        urlretrieve(ogs_url, data_filename)
        # extract the data
        if ext == ".tar.gz":
            z_file = tarfile.open(data_filename, "r:gz")
            names = z_file.getnames()
        else:
            z_file = zipfile.ZipFile(data_filename)
            names = z_file.namelist()
        file = ""
        for file in names:
            if os.path.basename(file).startswith("ogs"):
                break
        z_file.extract(member=file, path=tmpdirname)
        z_file.close()
        shutil.copy(os.path.join(tmpdirname, file), os.path.join(path, name))

"""
Downloadable datasets collected from various sources.

Once downloaded, these datasets are stored locally allowing for the
rapid reuse of these datasets.

Examples
--------
>>> from sigmaepsilon.core.downloads import download_stand
>>> download_stand()
...
"""

from functools import partial
import os
import shutil
from urllib.request import urlretrieve
import zipfile
from typing import Optional
from types import ModuleType

from .thirdparty import import_package
from . import EXAMPLES_PATH, SIGMAEPSILON_DATA_PATH as DATA_PATH

pyvista: Optional[ModuleType] = import_package("pyvista")


__all__ = ["download_file", "delete_downloads"]


def _check_examples_path():
    """Check if the examples path exists."""
    if not EXAMPLES_PATH:
        raise FileNotFoundError(
            "EXAMPLES_PATH does not exist. Try setting the "
            "environment variable `SIGMAEPSILON_USERDATA_PATH` "
            "to a writable path and restarting Python"
        )


def _decompress(filename):
    _check_examples_path()
    zip_ref = zipfile.ZipFile(filename, "r")
    zip_ref.extractall(EXAMPLES_PATH)
    return zip_ref.close()


def _get_vtk_file_url(filename):
    return f"https://github.com/sigma-epsilon/sigmaepsilon.data/raw/main/{filename}"


def _http_request(url):
    return urlretrieve(url)


def _repo_file_request(repo_path, filename):
    return os.path.join(repo_path, "Data", filename), None


def _retrieve_file(retriever, filename):
    """
    Retrieve file and cache it in sigmaepsilon.core.EXAMPLES_PATH.

    Parameters
    ----------
    retriever: str or callable
        If str, it is treated as a url.
        If callable, the function must take no arguments and must
        return a tuple like (file_path, resp), where file_path is
        the path to the file to use.
    filename: str
        The name of the file.

    Notes
    -----
    You must have `PyVista` installed to handle zip files.
    """
    _check_examples_path()
    # First check if file has already been downloaded
    local_path = os.path.join(EXAMPLES_PATH, os.path.basename(filename))
    local_path_no_zip = local_path.replace(".zip", "")
    if os.path.isfile(local_path_no_zip) or os.path.isdir(local_path_no_zip):
        return local_path_no_zip, None
    if isinstance(retriever, str):
        retriever = partial(_http_request, retriever)
    saved_file, resp = retriever()
    # new_name = saved_file.replace(os.path.basename(saved_file), os.path.basename(filename))
    # Make sure folder exists!
    if not os.path.isdir(os.path.dirname((local_path))):
        os.makedirs(os.path.dirname((local_path)))
    if DATA_PATH is None:
        shutil.move(saved_file, local_path)
    else:
        if os.path.isdir(saved_file):
            shutil.copytree(saved_file, local_path)
        else:
            shutil.copy(saved_file, local_path)
    if pyvista:
        if pyvista.get_ext(local_path) in [".zip"]:
            _decompress(local_path)
            local_path = local_path[:-4]
    return local_path, resp


def _download_file(filename):
    if DATA_PATH is None:
        url = _get_vtk_file_url(filename)
        retriever = partial(_http_request, url)
    else:
        if not os.path.isdir(DATA_PATH):
            raise FileNotFoundError(
                f"Data repository path does not exist at:\n\n{DATA_PATH}"
            )
        if not os.path.isdir(os.path.join(DATA_PATH, "Data")):
            raise FileNotFoundError(
                f'Data repository does not have "Data" folder at:\n\n{DATA_PATH}'
            )
        retriever = partial(_repo_file_request, DATA_PATH, filename)
    return _retrieve_file(retriever, filename)


def _download_and_read(filename):
    saved_file, _ = _download_file(filename)
    return saved_file


def download_file(filename: str) -> str:
    """
    Downloads a data file and returns the path of it on
    your local filesystem.

    Parameters
    ----------
    filename: str
        The name of the file to download with extension included.

    Returns
    -------
    str
        A path to a file on your filesystem.

    See also
    --------
    :func:`~sigmaepsilon.core.downloads.delete_downloads`

    Example
    --------
    >>> from sigmaepsilon.core.downloads import download_file
    >>> download_file("stand.vtk")
    """
    return _download_and_read(filename)


def delete_downloads() -> bool:
    """
    Delete all downloaded examples to free space or update the files.
    Returns `True` if the operation was succesful, or `False` if it wasn't.

    See also
    --------
    :func:`~sigmaepsilon.core.downloads.download_file`

    Examples
    --------
    Delete all local downloads.

    >>> from sigmaepsilon.core import delete_downloads
    >>> delete_downloads()  # doctest:+SKIP
    True
    """
    _check_examples_path()
    shutil.rmtree(EXAMPLES_PATH)
    os.makedirs(EXAMPLES_PATH)
    return True


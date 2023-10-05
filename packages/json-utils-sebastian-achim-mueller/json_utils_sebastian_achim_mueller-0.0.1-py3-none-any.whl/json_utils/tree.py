import glob
import os
import json_numpy
from .utils import read as read_single_json_file


def read(path):
    """
    Walks down a directory and reads every json-file into an object.

    Parameter
    ---------
    path : str
        Path of the directory to be read.

    Returns
    -------
    One combined object with the top-level keys beeing the dirnames
    and basenames of the json-files.
    """
    out = {}
    _paths = glob.glob(os.path.join(path, "*"))
    for _path in _paths:
        file_path, file_extension = os.path.splitext(_path)
        file_basename = os.path.basename(file_path)
        if str.lower(file_extension) == ".json":
            obj = read_single_json_file(_path)
            if isinstance(obj, list):
                tmp = numpy.array(obj)
                if tmp.dtype.str[1:] in json_numpy.VALID_DTYPES:
                    out[file_basename] = tmp
                else:
                    out[file_basename] = obj
            else:
                out[file_basename] = obj
        if os.path.isdir(_path):
            out[file_basename] = read(_path)
    return out

from __future__ import annotations

from typing import List, Dict, Any
import sys
import os
import inspect
import numpy as np  # pip install numpy

from airgen.client import MultirotorClient, VehicleClient, CarClient
from airgen.types import Vector3r, Quaternionr, ImageRequest, ImageType


def vector3d2list(vector3d: Vector3r) -> List[float]:
    """turn an AirGen Vector3r into a list of three floats

    Args:
        vector3d (Vector3r):

    Returns:
        List[float]:
    """
    return [vector3d.x_val, vector3d.y_val, vector3d.z_val]


def string_to_uint8_array(bstr: str | bytes) -> np.ndarray:
    """convert a string to a uint8 array

    Args:
        bstr (str|bytes):

    Returns:
        np.ndarray: numpy array with dtype uint8
    """
    return np.fromstring(bstr, np.uint8)


def string_to_float_array(bstr: str | bytes) -> np.ndarray:
    """convert a string to a float array

    Args:
        bstr (str|bytes): _description_

    Returns:
        np.ndarray:
    """
    return np.fromstring(bstr, np.float32)


def list_to_2d_float_array(flst: List[float], width: int, height: int) -> np.ndarray:
    """convert a list of floats to a 2d array

    Args:
        flst (List[float]):
        width (int):
        height (int):

    Returns:
        np.ndarray: numpy array with dtype=np.float32, shape=(height, width)
    """
    return np.reshape(np.asarray(flst, np.float32), (height, width))


def get_public_fields(obj) -> List[str]:
    """get all public fields of an object (not starting with _)

    Args:
        obj (Object):

    Returns:
        List[str]:
    """
    return [
        attr
        for attr in dir(obj)
        if not (
            attr.startswith("_")
            or inspect.isbuiltin(attr)
            or inspect.isfunction(attr)
            or inspect.ismethod(attr)
        )
    ]


def to_dict(obj) -> Dict[str, Any]:
    """Convert an object to a dictionary of its public fields

    Args:
        obj (Object):

    Returns:
        dic (Dict[str, Any]):
    """
    return dict([attr, getattr(obj, attr)] for attr in get_public_fields(obj))


def to_str(obj: object) -> str:
    """Convert an object to a string of its public fields

    Args:
        obj (object):

    Returns:
        str:
    """
    return str(to_dict(obj))


def write_file(filename, bstr):
    """
    Write binary data to file.
    Used for writing compressed PNG images
    """
    with open(filename, "wb") as afile:
        afile.write(bstr)


def wait_key(message=""):
    """Wait for a key press on the console and return it."""
    if message != "":
        print(message)

    result = None
    if os.name == "nt":
        import msvcrt

        result = msvcrt.getch()
    else:
        import termios

        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result

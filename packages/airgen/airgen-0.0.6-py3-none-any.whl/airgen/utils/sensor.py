from typing import List, Any, Literal, Tuple, Dict
import os
import sys
import re
import math
import numpy as np
import sys
import time
from functools import lru_cache

from airgen import airgen_logger
from airgen.types import ImageType, ImageResponse, ImageRequest
from .general import list_to_2d_float_array
from .mechanics import to_eularian_angles
from ._rgb2segid import rgb2segid
from ..client import VehicleClient


def imagetype2request(
    camera_name: Literal["front_center", "bottom_center"], image_type: ImageType
) -> ImageRequest:
    """helper function that creates uncompressed AirGen ImageRequest for image type

    Args:
        camera_name (Literal["front_center", "bottom_center"]):
        image_type (ImageType):

    Returns:
        ImageRequest:
    """
    # todo: assert camera_name is valid # in client connect, get all camera names
    if image_type in [
        ImageType.Scene,
        ImageType.Segmentation,
        ImageType.DepthVis,
        ImageType.OpticalFlowVis,
        ImageType.SurfaceNormals,
        ImageType.Infrared,
    ]:
        # uint8 type of `data
        return ImageRequest(camera_name, image_type, False, False)
    else:
        # float type of data
        return ImageRequest(camera_name, image_type, True, False)


def responses2images(
    responses: List[ImageResponse],
) -> List[Tuple[np.ndarray, Dict[str, Any]]]:
    """help function that converts a list of AirGen ImageResponse to a list of (image, camera_params) tuple


    Args:
        responses (List[ImageResponse]): list of AirGen ImageResponse

    Raises:
        ValueError: if response' image type is among listed below

    Returns:
        List[Tuple[np.ndarray, Dict[str, Any]]]: list of (image, camera_params) tuple

    image:
        * For ``ImageType.Scene``, ``ImageType.DepthVis``, ``ImageType.OpticalFlowVis``, image data is RGB image, numpy array with dtype=np.uint8, shape=(height, width, 3)
        * For ``ImageType.DepthPerspective``, ``ImageType.DepthPlanar``, ``ImageType.DisparityNormalized``, image data is depth image in meters, numpy array with dtype=np.float32, shape=(height, width, 1)
        * For ``ImageType.Segmentation``, image data is array of objects' SegmentationIDs, numpy array with dtype=np.uint8, shape=(height, width, 1)
        * For ``ImageType.SurfaceNormals``, image data is array of unit vector (normalized length), numpy array with dtype=np.float32, shape=(height, width, 3)
        * For ``ImageType.OpticalFlow``, image data is array of displacements in x,y directions, numpy array with dtype=np.float32, shape=(height, width, 2)
        * For ``ImageType.Infrared``, image data is array of infrared values (object's SegmentationID for now), numpy array with dtype=np.uint8, shape=(height, width, 1)

    camera parameters:
        * width (int): image width
        * height (int): image height
        * fov (float): camera field of view in degrees
        * camera_position (List[float]): camera position (x,y,z) in airgen (NED frame)
        * camera_orientation_euler_pry (List[float]): camera orientation (pitch, roll, yaw) in degrees
        * camera_orientation_quat_wxyz (List[float]): camera orientation (w,x,y,z) in quaternion format

    """
    res = []
    for response in responses:
        data = None
        image_type = response.image_type
        if image_type in [
            ImageType.Scene,
            ImageType.DepthVis,
            ImageType.Infrared,
            ImageType.SurfaceNormals,
            ImageType.OpticalFlowVis,
        ]:
            img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
            img_rgb = img1d.reshape(response.height, response.width, 3)
            if image_type == ImageType.SurfaceNormals:
                data = (img_rgb.astype(np.float32) / 255.0) * 2.0 - 1.0
                data = data / np.linalg.norm(data, axis=-1, keepdims=True)
            elif image_type == ImageType.Infrared:
                data = img_rgb[:, :, 0:1]  # keep the last dimension
            else:
                data = img_rgb
        elif image_type in [
            ImageType.DepthPerspective,
            ImageType.DepthPlanar,
            ImageType.DisparityNormalized,
        ]:
            depth_img_in_meters = np.reshape(
                np.asarray(response.image_data_float, dtype=np.float32),
                (response.width, response.height, 1),
            )
            data = depth_img_in_meters
        elif image_type == ImageType.Segmentation:
            img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
            segmentation_rgb = img1d.reshape(response.height, response.width, 3)
            data = RGB2SegmentationID(segmentation_rgb)
        elif image_type == ImageType.OpticalFlow:
            optical_flow = np.reshape(
                response.image_data_float, (response.width, response.height, 2)
            )
            data = optical_flow
        else:
            raise ValueError(f"image type {image_type} not recognized")
        camera_params = {}
        camera_params["image_type"] = image_type
        camera_params["width"] = response.width
        camera_params["height"] = response.height
        camera_params["camera_position"] = [
            response.camera_position.x_val,
            response.camera_position.y_val,
            response.camera_position.z_val,
        ]
        camera_params["camera_orientation_euler_pry"] = list(
            map(math.degrees, to_eularian_angles(response.camera_orientation))
        )
        camera_params["fov"] = response.camera_fov
        camera_params["camera_orientation_quat_wxyz"] = [
            response.camera_orientation.w_val,
            response.camera_orientation.x_val,
            response.camera_orientation.y_val,
            response.camera_orientation.z_val,
        ]
        res.append((data, camera_params))
    return res


def RGB2SegmentationID(RGB: np.ndarray) -> np.ndarray:
    """Map a airgen segmentation image (in rgb format) to 1-channel image of segmentation IDs"""
    seg = np.zeros((RGB.shape[0], RGB.shape[1], 1), dtype=np.uint8)
    # todo: vectorize this!
    for i in range(RGB.shape[0]):
        for j in range(RGB.shape[1]):
            seg_id = rgb2segid.get(tuple(RGB[i, j]), 256)

            if seg_id == 256:
                # airgen_logger.warning(
                #     "RGB value not found in mapping: %s, and it set to 255",
                #     str(RGB[i, j]),
                # )
                seg[i, j, 0] = 255
            else:
                seg[i, j, 0] = seg_id
    return seg


def compute_mapping_of_rgbgsegID() -> Tuple[dict, dict]:
    """re-compute mapping between rbg tuples to segmentation IDs by querying airgen

    Note:
        make sure airgen is running and the environment is loaded, and majority of the contents captured by front center camera is meaningful scene (not sky)

    Returns:
        Tuple[dict, dict]: segid2rgb, rgb2segid
    """
    client = VehicleClient(timeout_value=7200)
    client.confirmConnection()

    requests = ImageRequest("0", ImageType.Segmentation, False, False)

    # for
    id2rgb = {}
    rgb2id = {}
    for cls_id in range(256):
        # map every asset to cls_id and extract the single RGB value produced
        client.simSetSegmentationObjectID("[\w]*", cls_id, is_name_regex=True)
        time.sleep(2.0)
        response = client.simGetImages([requests])[0]
        img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
        img_rgb = img1d.reshape(response.height, response.width, 3)
        # find the most frequent rgb color
        img_2d = img_rgb.reshape(-1, 3)

        # Find the unique rows and their counts
        unique_rgb_values, unique_counts = np.unique(img_2d, axis=0, return_counts=True)

        # Find the index of the RGB value with the maximum count
        most_frequent_index = np.argmax(unique_counts)

        # color = tuple(np.unique(img_rgb.reshape(-1, img_rgb.shape[-1]), axis=0)[1])
        # in the env currently being tested, the sky is always 0
        color = tuple(unique_rgb_values[most_frequent_index])
        id2rgb[cls_id] = color
        rgb2id[color] = cls_id

    return id2rgb, rgb2id

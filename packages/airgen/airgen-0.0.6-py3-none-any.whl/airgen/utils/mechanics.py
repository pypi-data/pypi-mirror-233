from typing import Tuple, List, Optional, Any, Dict
import math

import ivy
import ivy_vision
import ivy_mech
import numpy as np
import rerun as rr

# for some ivy version, it is `ivt.set_framework('numpy')`
if hasattr(ivy, "set_framework"):
    ivy.set_framework("numpy")
elif hasattr(ivy, "set_backend"):
    ivy.set_backend("numpy")
else:
    raise ValueError("ivy does not support set_framework or set_backend")

NP_FLOATING_TYPE = np.float32

from airgen.types import Quaternionr


# ref: https:#en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
def to_eularian_angles(q: Quaternionr) -> Tuple[float, float, float]:
    """transform from quaternion to euler angles

    Args:
        q (Quaternionr): quaternion in wxyz format

    Returns:
        Tuple[float, float, float]: pitch, roll, yaw in radians
    """
    z = q.z_val
    y = q.y_val
    x = q.x_val
    w = q.w_val
    ysqr = y * y

    # roll (x-axis rotation)
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + ysqr)
    roll = math.atan2(t0, t1)

    # pitch (y-axis rotation)
    t2 = +2.0 * (w * y - z * x)
    if t2 > 1.0:
        t2 = 1
    if t2 < -1.0:
        t2 = -1.0
    pitch = math.asin(t2)

    # yaw (z-axis rotation)
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (ysqr + z * z)
    yaw = math.atan2(t3, t4)

    return (pitch, roll, yaw)


def to_quaternion(pitch: float, roll: float, yaw: float) -> Quaternionr:
    """transform from euler angles to quaternion

    Args:
        pitch (float): pitch in radians. Positive pitch means tilt upward
        roll (float): roll in radians
        yaw (float): roll in radians

    Returns:
        Quaternior: quaternion representation of the euler angles
    """
    t0 = math.cos(yaw * 0.5)
    t1 = math.sin(yaw * 0.5)
    t2 = math.cos(roll * 0.5)
    t3 = math.sin(roll * 0.5)
    t4 = math.cos(pitch * 0.5)
    t5 = math.sin(pitch * 0.5)

    q = Quaternionr()
    q.w_val = t0 * t2 * t4 + t1 * t3 * t5  # w
    q.x_val = t0 * t3 * t4 - t1 * t2 * t5  # x
    q.y_val = t0 * t2 * t5 + t1 * t3 * t4  # y
    q.z_val = t1 * t2 * t4 - t0 * t3 * t5  # z
    return q


def homo_coord_to_nonhome_coord(home_coord: ivy.Array) -> ivy.Array:
    """turn homogeneous coordinates to non-homogeneous coordinates (factoring out the last dimension)

    Args:
        home_coord (ivy.Array): of shape (..., n)

    Returns:
        ivy.Array: of shape (..., n-1)
    """
    non_home_coord = home_coord / home_coord[..., -1][..., None]
    return non_home_coord[..., :-1]


def cameracoord2worldcoord(
    camera_coord: List[float], camera_params: dict
) -> np.ndarray:
    """given airgen camera parameters, transform  camera coordinate back to airgen world coordinate

    Args:
        camera_coord (List[float]): (x,y,z)
        camera_params (dict): camera parameters

    Returns:
        np.ndarray: _description_
    """
    cam_inv_ext_mat = build_camera_inv_extrinsic(camera_params=camera_params)
    world_coord = ivy_vision.cam_to_world_coords(camera_coord, cam_inv_ext_mat)[
        ..., 0:3
    ]
    return world_coord


def quat_wxyz_to_xyzw(quat_wxyz: List[float]) -> np.ndarray:
    """transform quaternion (represented by list of floats) from wxyz format to xyzw format

    Args:
        quat_wxyz (List[Float]):

    Returns:
        np.ndarray: quaternion in xyzw format
    """
    return np.array(
        [quat_wxyz[1], quat_wxyz[2], quat_wxyz[3], quat_wxyz[0]], dtype=NP_FLOATING_TYPE
    )


def build_camera_intrinsic(camera_params: dict) -> ivy_vision.Intrinsics:
    """given airgen camera parameters, build camera intrinsic matrix

    Args:
        camera_params (dict): aigen camera parameters

    Returns:
        ivy_vision.Intrinsics:
    """
    pp_offset = np.array(
        [item / 2 - 0.5 for item in [camera_params["width"], camera_params["height"]]],
        dtype=NP_FLOATING_TYPE,
    )
    persp_angle = np.array(
        [camera_params["fov"] * np.pi / 180] * 2, dtype=NP_FLOATING_TYPE
    )
    intrinsic = ivy_vision.persp_angles_and_pp_offsets_to_intrinsics_object(
        persp_angle, pp_offset, [camera_params["width"], camera_params["height"]]
    )
    return intrinsic


def build_camera_inv_extrinsic(camera_params: dict) -> ivy.Array:
    """given airgen camera parameters, build camera inverse extrinsic matrix

    Args:
        camera_params (dict): airgen camera parameters

    Returns:
        ivy.Array: inverse of camera extrinsic matrix
    """
    cam_position = np.array(camera_params["camera_position"], dtype=NP_FLOATING_TYPE)
    cam_quaternion = quat_wxyz_to_xyzw(camera_params["camera_orientation_quat_wxyz"])
    cam_quat_poses = ivy.concat((cam_position, cam_quaternion), axis=-1)

    cam_inv_ext_mat = ivy_mech.quaternion_pose_to_mat_pose(cam_quat_poses)
    return cam_inv_ext_mat


def build_camera(camera_params: dict) -> Tuple[ivy.Array, ivy.Array]:
    """given airgen camera parameters, build camera inverse extrinsic matrix and camera intrinsic matrix

    Args:
        camera_params (dict): airgen camera parameters

    Returns:
        Tuple[ivy.Array, ivy.Array]: inverse of camera extrinsic matrix and inverse of camera calibration matrix
    """
    intrinsic = build_camera_intrinsic(camera_params)
    cam_inv_calib_mat = intrinsic.inv_calib_mats
    cam_inv_ext_mat = build_camera_inv_extrinsic(camera_params)
    return cam_inv_ext_mat, cam_inv_calib_mat


def camera_unproject_depth(
    depth: np.ndarray, cam_inv_ext_mat: ivy.Array, cam_inv_calib_mat: ivy.Array
) -> np.ndarray:
    """generate point cloud from depth image (depth perspective)

    Args:
        depth (np.ndarray): of shape (H, W, 1)
        cam_inv_ext_mat (ivy.Array): inverse of camera extrinsic matrix
        cam_inv_calib_mat (ivy.Array): inverse of camera intrinsic matrix

    Returns:
        np.ndarray: point cloud of shape (N, 3)
    """
    uniform_pixel_coords = ivy_vision.create_uniform_pixel_coords_image(
        image_dims=(depth.shape[0], depth.shape[1])
    )

    cam_coords = ivy_vision.ds_pixel_to_cam_coords(
        uniform_pixel_coords,
        cam_inv_calib_mat,
        [],
        image_shape=(depth.shape[0], depth.shape[1]),
    )
    # normalize the (non-homogeneous) part of camera coordinates to have unit norm and then scale by depth
    cam_coords[..., :-1] = (
        cam_coords[..., :-1]
        / np.linalg.norm(cam_coords[..., :-1], axis=-1, keepdims=True)
    ) * depth
    # camera coordinate to ned
    camera2ned = np.array(
        [[0, -1, 0, 0], [0, 0, -1, 0], [1, 0, 0, 0], [0, 0, 0, 1]],
        dtype=cam_coords.dtype,
    )
    # which is the transpose of
    # camera2ned = np.transpose(
    #     np.array(
    #         [[0, 0, 1, 0], [-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 0, 1]],
    #         dtype=cam_coords.dtype,
    #     )
    # )
    ned_coords = np.dot(cam_coords, camera2ned)
    return ivy_vision.cam_to_world_coords(ned_coords, cam_inv_ext_mat)[..., 0:3]


def imagecoord2orientation(pixelcoord, camera_param) -> Tuple[float, float, float]:
    """Given camera parameters (position, pose, and fov) and  pixel coordinate, return the 3D direction of the pixel
    with respect to the camera represented in yaw and pitch (absolute degrees)

    Args:
        pixelcoord (Tuple[float, float]): coordinate of the pixel in the image in xy format
        camera_param (Dict[str, Any]): camera parameters

    Returns:
        Tuple[float, float float]: target pitch, roll, yaw in radians
    """
    delta_yaw = (
        (pixelcoord[0] - camera_param["width"] / 2)
        / camera_param["width"]
        * camera_param["fov"]
    )

    delta_pitch = (
        (camera_param["height"] / 2 - pixelcoord[1])
        / camera_param["height"]
        * 2
        * math.degrees(
            math.atan(
                math.tan(math.radians(camera_param["fov"] / 2))
                / (camera_param["width"] / camera_param["height"])
            )
        )
    )
    target_yaw, target_pitch = (
        math.radians(camera_param["camera_orientation_euler_pry"][2] + delta_yaw),
        math.radians(camera_param["camera_orientation_euler_pry"][0] + delta_pitch),
    )
    return (target_pitch, 0, target_yaw)


def imagecoord2direction(
    pixelcoord: Tuple[float, float], camera_param: Dict[str, Any]
) -> Tuple[float, float, float]:
    """Given camera parameters (position, pose, and fov) and  pixel coordinate, return the 3D direction of the pixel
    with respect to the camera

    Args:
        pixelcoord (Tuple[float, float]): coordinate of the pixel in the image in xy format
        camera_param (Dict[str, Any]): camera parameters

    Returns:
        Tuple[float, float, float]: normalized unit (directional) vector (x, y, z)
    """
    target_pitch, _, target_yaw = imagecoord2orientation(pixelcoord, camera_param)
    target_direction = pose2vector(target_pitch, 0, target_yaw)

    return target_direction


def pose2vector(pitch: float, roll: float, yaw: float) -> Tuple[float, float, float]:
    """transform target direction represnted in (pitch, roll, yaw) in radians to directional vector

    Args:
        pitch (float): in radians
        roll (float): in radians
        yaw (float): in radians

    Returns:
        Tuple[float, float, float]: unit directional vector (x,y,z)
    """
    vector = [
        math.cos(pitch) * math.cos(yaw),
        math.cos(pitch) * math.sin(yaw),
        -math.sin(pitch),
    ]
    return vector


def imagecoord2pose(
    pixelcoord: Tuple[float, float], point_depth: float, camera_param: Dict[str, Any]
) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
    """convert pixel coordinate to 3D coordinate

    Args:
        pixelcoord (Tuple[float, float]): coordinate of the pixel in the image in xy format
        point_depth (float): depth of the point
        camera_param (Dict[str, Any]): camera parameters

    Returns:
        Tuple[float, float, float]: target coordinate in (x, y, z)
        Tuple[float, float, float]: target orientation in (pitch, roll, yaw) in radians
    """
    target_pitch, _, target_yaw = imagecoord2orientation(pixelcoord, camera_param)
    target_direction = pose2vector(target_pitch, 0, target_yaw)
    target_coord = (
        np.array(target_direction) * point_depth + camera_param["camera_position"]
    )
    return target_coord, (target_pitch, 0, target_yaw)


def vec2eulerangles(vec: np.ndarray) -> np.ndarray:
    """transform airgen directional vector to euler angles

    Args:
        vec: directional vector of shape (N, 3)

    Returns:
        np.ndarray: euler angles of shape (N, 3), each row is (pitch, roll, yaw) in degrees
    """

    yaw = np.rad2deg(np.arctan2(vec[:, 1], vec[:, 0]))
    pitch = np.rad2deg(
        np.arctan2(-vec[:, 2], np.sqrt(np.square(vec[:, 0]) + np.square(vec[:, 1])))
    )
    return np.stack([pitch, np.zeros_like(pitch), yaw], axis=1)


def depth2pointcloud(
    depth: np.ndarray,
    camera_param: dict,
    mask: Optional[np.ndarray] = None,
) -> np.ndarray:
    """generating point cloud from depth image

    Args:
        depth (np.ndarray): depth image of shape (H, W, 1)
        camera_param (dict): camera parameters that contains fov, height, width and camera pose
        mask (Optional[np.ndarray], optional): boolean (0/1) mask where 1 indicates object of interest, (H, W, 1). Defaults to None.

    Returns:
        np.ndarray: point cloud in airgen world coordinate of shape (N, 3)
    """

    camera_inv_ext_mat, camera_inv_calib_mat = build_camera(camera_param)
    point_cloud = camera_unproject_depth(
        depth=depth,
        cam_inv_ext_mat=camera_inv_ext_mat,
        cam_inv_calib_mat=camera_inv_calib_mat,
    )

    if mask is not None:
        point_cloud = point_cloud[np.where(mask.squeeze(-1) > 0.5)]

    point_cloud = point_cloud.reshape((-1, 3))

    return point_cloud.to_numpy()


def rotate_xy(vec: np.ndarray, theta: float) -> np.ndarray:
    """rotate xy-component of 3d vector by theta (in degrees) counter-clockwise (in xy plane)

    Assume looking from positive z-axis, the orientation is

    ::

        ^ y
        |
        |
        |______> x

    Args:
        vec (np.ndarray): shape (3,)
        theta (float): angles in degrees

    Returns:
        np.ndarray: rotated vector shape (3,)
    """
    theta_radians = 2 * math.pi - math.radians(theta)
    rotation_matrix = np.array(
        [
            [math.cos(theta_radians), -math.sin(theta_radians), 0],
            [math.sin(theta_radians), math.cos(theta_radians), 0],
            [0, 0, 1],
        ],
        dtype=vec.dtype,
    )
    rotated_vec = np.dot(rotation_matrix, vec)
    return rotated_vec

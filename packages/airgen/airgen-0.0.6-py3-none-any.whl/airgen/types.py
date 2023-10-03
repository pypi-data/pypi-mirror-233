from __future__ import print_function
from typing import List, Tuple
import msgpackrpc  #
import numpy as np  # pip install numpy
import math


class MsgpackMixin:
    def __repr__(self):
        from pprint import pformat

        return "<" + type(self).__name__ + "> " + pformat(vars(self), indent=4, width=1)

    def to_msgpack(self, *args, **kwargs):
        return self.__dict__

    @classmethod
    def from_msgpack(cls, encoded):
        obj = cls()
        # obj.__dict__ = {k.decode('utf-8'): (from_msgpack(v.__class__, v) if hasattr(v, "__dict__") else v) for k, v in encoded.items()}
        obj.__dict__ = {
            k: (
                v
                if not isinstance(v, dict)
                else getattr(getattr(obj, k).__class__, "from_msgpack")(v)
            )
            for k, v in encoded.items()
        }
        # return cls(**msgpack.unpack(encoded))
        return obj


class _ImageType(type):
    @property
    def Scene(cls):
        return 0

    def DepthPlanar(cls):
        return 1

    def DepthPerspective(cls):
        return 2

    def DepthVis(cls):
        return 3

    def DisparityNormalized(cls):
        return 4

    def Segmentation(cls):
        return 5

    def SurfaceNormals(cls):
        return 6

    def Infrared(cls):
        return 7

    def OpticalFlow(cls):
        return 8

    def OpticalFlowVis(cls):
        return 9

    def __getattr__(self, key):
        if key == "DepthPlanner":
            print(
                "\033[31m"
                + "DepthPlanner has been (correctly) renamed to DepthPlanar. Please use ImageType.DepthPlanar instead."
                + "\033[0m"
            )
            raise AttributeError


class ImageType(metaclass=_ImageType):
    """
    Image types supported by AirGen.

    Default settings of camera type in settings.json
    ::

        {
            "CameraDefaults": {
                "CaptureSettings": [
                    "ImageType": 0,
                    "Width": 256,
                    "Height": 256,
                    "FOV_Degrees": 90,
                    "AutoExposureSpeed": 100.0,
                    "AutoExposureBias": 0,
                    "MotionBlurAmount": 0.0,
                    "MotionBlurMaxDistortion": 0.0,
                    "TargetGamma": 1.0
                    }
                ]
            }
        }

    example code:
    .. todo:: add link to example script for cameras
    """

    Scene = 0
    """
    description\uFF1A RGB image

    pertinent parameters in ImageRequest:
        * pixels_as_float: False

    image data stored as numpy array with dtype:uint8 array with shape:[height, width, 3]
    """
    DepthPlanar = 1
    """
    description\uFF1A distance between object and camera's imaging plane, i.e., all points that are plane-parallel to the camera have same depth

    pertinent parameters in ImageRequest:
        * pixels_as_float: True
        * compress: False

    image data stored as numpy array with dtype:np.float32 and shape:[height, width, 1]
    """
    DepthPerspective = 2
    """
    decription\uFF1A distance between object and camera's focal point. This is suitable for point cloud reconstruction.
    
    pertinent parameters in ImageRequest:
        * pixels_as_float: True
        * compress: False

    image data stored as numpy array with dtype:np.float32 and shape:[height, width, 1]
    """
    DepthVis = 3
    """
    description\uFF1A encodes depth info into RGB channels for visualization. Each pixel value is interpolated from black to white depending on depth in camera plane in meters. The pixels with pure white means depth of 100m or more while pure black means depth of 0 meters.

    pertinent parameters in ImageRequest:
        * pixels_as_float: False
    
    image stored as numpy array with dtype:uint8 and shape: [height, width, 3]
    """
    DisparityNormalized = 4
    """
    description\uFF1A normalized disparity, each pixel is `(Xl - Xr)/Xmax`, which is thereby normalized to values between 0 to 1.

    pertinent parameters in ImageRequest:
        * pixels_as_float: True
        * compress: False
    
    image data stored as numpy array with dtype=np.float32 and shape:[height, width, 1]
    """
    Segmentation = 5
    """
    descritpion\uFF1A RGB image where each pixel encodes a unique Segmentation ID of object. It is recommended that you request uncompressed image using this API
    
    pertinent parameters in ImageRequest:
        * pixels_as_float: False
        * compress: False

    image data stored as numpy array with dtype:uint8 and shape:[height, width, 3]
    """
    SurfaceNormals = 6
    """
    description\uFF1A surface normals of objects in the scene encoded into RGB channels. To get unit vector of the normal, use the following formula:
    .. math::
        
        x = (r / 255)*2.0 - 1.0
        y = (g / 255)*2.0 - 1.0
        z = (b / 255)*2.0 - 1.0

    pertinent parameters in ImageRequest:
        * pixels_as_float: False
        
    image data stored as numpy array with dtype:uint8 and shape:[height, width, 3]
    """
    Infrared = 7
    """ 
    description\uFF1A Currently this is just a map from object's SegmentationID to grey scale 0-255. So any mesh with object ID 42 shows up with color (42, 42, 42).
    
    pertinent parameters in ImageRequest:
        * pixels_as_float: False

    image data stored as numpy array with dtype:uint8 and shape:[height, width, 3]
    """
    OpticalFlow = 8
    """
    description\uFF1A optical flow, information about motion perceived by the point of view of the camera of the scene. OpticalFlow returns a 2-channel image where the channels correspond to vx and vy respectively.
    
    pertinent parameters in ImageRequest:
        * pixels_as_float: True
        * compress: False

    image data stored as numpy array with dtype:np.float32 and shape:[height, width, 2]
    """
    OpticalFlowVis = 9
    """
    description\uFF1A encodes optical flow into RGB channels for visualization

    pertinent parameters in ImageRequest:
        * pixels_as_float: False

    image data stored as numpy array with dtype:uint8 and shape:[height, width, 3]
    """

    @staticmethod
    def to_str(image_type: int) -> str:
        """convert image type to string

        Args:
            image_type (int): _description_

        Returns:
            str: _description_
        """
        if image_type == ImageType.Scene:
            return "Scene"
        elif image_type == ImageType.DepthPlanar:
            return "DepthPlanar"
        elif image_type == ImageType.DepthPerspective:
            return "DepthPerspective"
        elif image_type == ImageType.DepthVis:
            return "DepthVis"
        elif image_type == ImageType.DisparityNormalized:
            return "DisparityNormalized"
        elif image_type == ImageType.Segmentation:
            return "Segmentation"
        elif image_type == ImageType.SurfaceNormals:
            return "SurfaceNormals"
        elif image_type == ImageType.Infrared:
            return "Infrared"
        elif image_type == ImageType.OpticalFlow:
            return "OpticalFlow"
        elif image_type == ImageType.OpticalFlowVis:
            return "OpticalFlowVis"
        else:
            raise ValueError(f"image type {image_type} not supported")


class DrivetrainType:
    MaxDegreeOfFreedom = 0
    ForwardOnly = 1


class LandedState:
    Landed = 0
    Flying = 1


class WeatherParameter:
    Rain = 0
    Roadwetness = 1
    Snow = 2
    RoadSnow = 3
    MapleLeaf = 4
    RoadLeaf = 5
    Dust = 6
    Fog = 7
    Enabled = 8


class Vector2r(MsgpackMixin):
    """Airgen Vector2r class that represents 2d vector, mainly used for parameters in simAPI calls."""

    x_val = 0.0
    y_val = 0.0

    def __init__(self, x_val=0.0, y_val=0.0):
        self.x_val = x_val
        self.y_val = y_val


class Vector3r(MsgpackMixin):
    """Airgen Vector3r class that represents 3d vector, mainly used for parameters in simAPI calls."""

    x_val = 0.0
    y_val = 0.0
    z_val = 0.0

    def __init__(self, x_val=0.0, y_val=0.0, z_val=0.0):
        self.x_val = x_val
        self.y_val = y_val
        self.z_val = z_val

    @staticmethod
    def nanVector3r():
        return Vector3r(np.nan, np.nan, np.nan)

    def containsNan(self):
        return (
            math.isnan(self.x_val) or math.isnan(self.y_val) or math.isnan(self.z_val)
        )

    def __add__(self, other):
        return Vector3r(
            self.x_val + other.x_val, self.y_val + other.y_val, self.z_val + other.z_val
        )

    def __sub__(self, other):
        return Vector3r(
            self.x_val - other.x_val, self.y_val - other.y_val, self.z_val - other.z_val
        )

    def __truediv__(self, other):
        if (
            type(other)
            in [int, float]
            + np.sctypes["int"]
            + np.sctypes["uint"]
            + np.sctypes["float"]
        ):
            return Vector3r(self.x_val / other, self.y_val / other, self.z_val / other)
        else:
            raise TypeError(
                "unsupported operand type(s) for /: %s and %s"
                % (str(type(self)), str(type(other)))
            )

    def __mul__(self, other):
        if (
            type(other)
            in [int, float]
            + np.sctypes["int"]
            + np.sctypes["uint"]
            + np.sctypes["float"]
        ):
            return Vector3r(self.x_val * other, self.y_val * other, self.z_val * other)
        else:
            raise TypeError(
                "unsupported operand type(s) for *: %s and %s"
                % (str(type(self)), str(type(other)))
            )

    def dot(self, other):
        if type(self) == type(other):
            return (
                self.x_val * other.x_val
                + self.y_val * other.y_val
                + self.z_val * other.z_val
            )
        else:
            raise TypeError(
                "unsupported operand type(s) for 'dot': %s and %s"
                % (str(type(self)), str(type(other)))
            )

    def cross(self, other):
        if type(self) == type(other):
            cross_product = np.cross(self.to_numpy_array(), other.to_numpy_array())
            return Vector3r(cross_product[0], cross_product[1], cross_product[2])
        else:
            raise TypeError(
                "unsupported operand type(s) for 'cross': %s and %s"
                % (str(type(self)), str(type(other)))
            )

    def get_length(self):
        return (self.x_val**2 + self.y_val**2 + self.z_val**2) ** 0.5

    def distance_to(self, other):
        return (
            (self.x_val - other.x_val) ** 2
            + (self.y_val - other.y_val) ** 2
            + (self.z_val - other.z_val) ** 2
        ) ** 0.5

    def to_Quaternionr(self):
        return Quaternionr(self.x_val, self.y_val, self.z_val, 0)

    def to_numpy_array(self):
        return np.array([self.x_val, self.y_val, self.z_val], dtype=np.float32)

    def __iter__(self):
        return iter((self.x_val, self.y_val, self.z_val))


class Quaternionr(MsgpackMixin):
    """Airgen's representation of quaternion in wxyz format."""

    w_val = 0.0
    x_val = 0.0
    y_val = 0.0
    z_val = 0.0

    def __init__(self, w_val=1.0, x_val=0.0, y_val=0.0, z_val=0.0):
        self.w_val = w_val
        self.x_val = x_val
        self.y_val = y_val
        self.z_val = z_val

    @staticmethod
    def nanQuaternionr():
        return Quaternionr(np.nan, np.nan, np.nan, np.nan)

    def containsNan(self):
        return (
            math.isnan(self.w_val)
            or math.isnan(self.x_val)
            or math.isnan(self.y_val)
            or math.isnan(self.z_val)
        )

    def __add__(self, other):
        if type(self) == type(other):
            return Quaternionr(
                self.x_val + other.x_val,
                self.y_val + other.y_val,
                self.z_val + other.z_val,
                self.w_val + other.w_val,
            )
        else:
            raise TypeError(
                "unsupported operand type(s) for +: %s and %s"
                % (str(type(self)), str(type(other)))
            )

    def __mul__(self, other):
        if type(self) == type(other):
            t, x, y, z = self.w_val, self.x_val, self.y_val, self.z_val
            a, b, c, d = other.w_val, other.x_val, other.y_val, other.z_val
            return Quaternionr(
                w_val=a * t - b * x - c * y - d * z,
                x_val=b * t + a * x + d * y - c * z,
                y_val=c * t + a * y + b * z - d * x,
                z_val=d * t + z * a + c * x - b * y,
            )
        else:
            raise TypeError(
                "unsupported operand type(s) for *: %s and %s"
                % (str(type(self)), str(type(other)))
            )

    def __truediv__(self, other):
        if type(other) == type(self):
            return self * other.inverse()
        elif (
            type(other)
            in [int, float]
            + np.sctypes["int"]
            + np.sctypes["uint"]
            + np.sctypes["float"]
        ):
            return Quaternionr(
                self.x_val / other,
                self.y_val / other,
                self.z_val / other,
                self.w_val / other,
            )
        else:
            raise TypeError(
                "unsupported operand type(s) for /: %s and %s"
                % (str(type(self)), str(type(other)))
            )

    def dot(self, other):
        if type(self) == type(other):
            return (
                self.x_val * other.x_val
                + self.y_val * other.y_val
                + self.z_val * other.z_val
                + self.w_val * other.w_val
            )
        else:
            raise TypeError(
                "unsupported operand type(s) for 'dot': %s and %s"
                % (str(type(self)), str(type(other)))
            )

    def cross(self, other):
        if type(self) == type(other):
            return (self * other - other * self) / 2
        else:
            raise TypeError(
                "unsupported operand type(s) for 'cross': %s and %s"
                % (str(type(self)), str(type(other)))
            )

    def outer_product(self, other):
        if type(self) == type(other):
            return (self.inverse() * other - other.inverse() * self) / 2
        else:
            raise TypeError(
                "unsupported operand type(s) for 'outer_product': %s and %s"
                % (str(type(self)), str(type(other)))
            )

    def rotate(self, other):
        if type(self) == type(other):
            if other.get_length() == 1:
                return other * self * other.inverse()
            else:
                raise ValueError("length of the other Quaternionr must be 1")
        else:
            raise TypeError(
                "unsupported operand type(s) for 'rotate': %s and %s"
                % (str(type(self)), str(type(other)))
            )

    def conjugate(self):
        return Quaternionr(-self.x_val, -self.y_val, -self.z_val, self.w_val)

    def star(self):
        return self.conjugate()

    def inverse(self):
        return self.star() / self.dot(self)

    def sgn(self):
        return self / self.get_length()

    def get_length(self):
        return (
            self.x_val**2 + self.y_val**2 + self.z_val**2 + self.w_val**2
        ) ** 0.5

    def to_numpy_array(self):
        return np.array(
            [self.x_val, self.y_val, self.z_val, self.w_val], dtype=np.float32
        )

    def __iter__(self):
        return iter((self.x_val, self.y_val, self.z_val, self.w_val))

    @property
    def xyzw(self) -> Tuple[float, float, float, float]:
        """return the quaternion as a tuple (x, y, z, w)


        Returns:
            Tuple[float, float, float, float]: (x, y, z, w)
        """
        return (self.x_val, self.y_val, self.z_val, self.w_val)

    @property
    def wxyz(self) -> Tuple[float, float, float, float]:
        """return the quaternion as a tuple (w, x, y, z)

        Returns:
            Tuple[float, float, float, float]: (w, x, y, z)
        """
        return (self.w_val, self.x_val, self.y_val, self.z_val)


class Pose(MsgpackMixin):
    position = Vector3r()
    orientation = Quaternionr()

    def __init__(self, position_val=None, orientation_val=None):
        position_val = position_val if position_val is not None else Vector3r()
        orientation_val = (
            orientation_val if orientation_val is not None else Quaternionr()
        )
        self.position = position_val
        self.orientation = orientation_val

    @staticmethod
    def nanPose():
        return Pose(Vector3r.nanVector3r(), Quaternionr.nanQuaternionr())

    def containsNan(self):
        return self.position.containsNan() or self.orientation.containsNan()

    def __iter__(self):
        return iter((self.position, self.orientation))


class CollisionInfo(MsgpackMixin):
    has_collided = False
    normal = Vector3r()
    impact_point = Vector3r()
    position = Vector3r()
    penetration_depth = 0.0
    time_stamp = 0.0
    object_name = ""
    object_id = -1


class GeoPoint(MsgpackMixin):
    latitude = 0.0
    longitude = 0.0
    altitude = 0.0

    def __init__(self, latitude=0.0, longitude=0.0, altitude=0.0):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

class GeoPose(MsgpackMixin):
    geopoint = GeoPoint()
    orientation = Quaternionr()

    def __init__(self, geopoint_val: GeoPoint = None, orientation_val: Quaternionr = None):
        self.geopoint = geopoint_val
        self.orientation = orientation_val

class YawMode(MsgpackMixin):
    is_rate = True
    yaw_or_rate = 0.0

    def __init__(self, is_rate=True, yaw_or_rate=0.0):
        self.is_rate = is_rate
        self.yaw_or_rate = yaw_or_rate


class RCData(MsgpackMixin):
    timestamp = 0
    pitch, roll, throttle, yaw = (0.0,) * 4  # init 4 variable to 0.0
    switch1, switch2, switch3, switch4 = (0,) * 4
    switch5, switch6, switch7, switch8 = (0,) * 4
    is_initialized = False
    is_valid = False

    def __init__(
        self,
        timestamp=0,
        pitch=0.0,
        roll=0.0,
        throttle=0.0,
        yaw=0.0,
        switch1=0,
        switch2=0,
        switch3=0,
        switch4=0,
        switch5=0,
        switch6=0,
        switch7=0,
        switch8=0,
        is_initialized=False,
        is_valid=False,
    ):
        self.timestamp = timestamp
        self.pitch = pitch
        self.roll = roll
        self.throttle = throttle
        self.yaw = yaw
        self.switch1 = switch1
        self.switch2 = switch2
        self.switch3 = switch3
        self.switch4 = switch4
        self.switch5 = switch5
        self.switch6 = switch6
        self.switch7 = switch7
        self.switch8 = switch8
        self.is_initialized = is_initialized
        self.is_valid = is_valid


class ImageRequest(MsgpackMixin):
    """A class to facilitate image capture requests in AirGen."""

    camera_name: str = "front_center"
    """description\uFF1A name of the camera.

    For car, the default camera names are: ``front_center``, ``front_right``, ``front_left``, ``back_center``, ``fpv``, ``back_center``. ``fpv`` camera is driver's head position in the car.

    For multirotor, the default camera names are: ``front_center``, ``front_right``, ``front_left``, ``bottom_center``.
    
    In computer vision mode, camera names are same as in multirotor.

    Apart from these, you can add more cameras to the vehicles and external cameras which are not attached to any vehicle through the settings.json file.
    """
    image_type: ImageType = ImageType.Scene
    pixels_as_float: bool = False
    """
    if true, image pixels are returned as float, else as uint8. Check `ImageType` for the proper parameters of each image type"""
    compress: bool = False
    """
    if true, image is compressed using jpg, else uncompressed png. Cannot be true when `pixels_as_float` is true.
    Check `ImageType` for the proper parameters of each image type
    """

    def __init__(
        self,
        camera_name: str,
        image_type: ImageType,
        pixels_as_float=False,
        compress=True,
    ):
        # todo: in future remove str(), it's only for compatibility to pre v1.2
        self.camera_name = str(camera_name)
        self.image_type = image_type
        self.pixels_as_float = pixels_as_float
        self.compress = compress
        assert not (pixels_as_float and compress), "cannot compress float images"
        if image_type in [
            ImageType.Scene,
            ImageType.DepthVis,
            ImageType.Segmentation,
            ImageType.SurfaceNormals,
            ImageType.Infrared,
            ImageType.OpticalFlowVis,
        ]:
            assert not pixels_as_float, f"{image_type} images cannot be float"
        elif image_type in [
            ImageType.DepthPerspective,
            ImageType.DepthPlanar,
            ImageType.DisparityNormalized,
            ImageType.OpticalFlow,
        ]:
            assert pixels_as_float, f"{image_type} images must be float"
        else:
            raise ValueError(f"unknown image type {image_type}")


class ImageResponse(MsgpackMixin):
    """
    A class to handle and represent image responses from AirGen.
    """

    image_data_uint8: bytes = bytes()
    """
    description\uFF1A uint8 image data stored in raw bytes. Empty if pixels_as_float is true.

    usage::

    >>> img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) # get 1d numpy array
    >>> img_rgb = img1d.reshape(response.height, response.width, 3) # reshape to 3 channel image array H X W X 3
    """
    image_data_float: List[float] = []
    """
    description\uFF1A float image data stored in raw bytes. Empty if pixels_as_float is false.
    
    usage::

    >>> img1d = np.asarray(response.image_data_float, dtype=np.float32)
    >>> img = img1d.reshape(response.height, response.width, num_channels) 
    """
    camera_position: Vector3r = Vector3r()
    camera_orientation: Quaternionr = Quaternionr()
    camera_fov: float = 0.0
    time_stamp = np.uint64(0)
    message: str = ""
    pixels_as_float: bool = False
    compress: float = True
    width: int = 0
    height: int = 0
    image_type: ImageType = ImageType.Scene


class CarControls(MsgpackMixin):
    throttle = 0.0
    steering = 0.0
    brake = 0.0
    handbrake = False
    is_manual_gear = False
    manual_gear = 0
    gear_immediate = True

    def __init__(
        self,
        throttle=0,
        steering=0,
        brake=0,
        handbrake=False,
        is_manual_gear=False,
        manual_gear=0,
        gear_immediate=True,
    ):
        self.throttle = throttle
        self.steering = steering
        self.brake = brake
        self.handbrake = handbrake
        self.is_manual_gear = is_manual_gear
        self.manual_gear = manual_gear
        self.gear_immediate = gear_immediate

    def set_throttle(self, throttle_val, forward):
        if forward:
            self.is_manual_gear = False
            self.manual_gear = 0
            self.throttle = abs(throttle_val)
        else:
            self.is_manual_gear = False
            self.manual_gear = -1
            self.throttle = -abs(throttle_val)


class KinematicsState(MsgpackMixin):
    position = Vector3r()
    orientation = Quaternionr()
    linear_velocity = Vector3r()
    angular_velocity = Vector3r()
    linear_acceleration = Vector3r()
    angular_acceleration = Vector3r()


class EnvironmentState(MsgpackMixin):
    position = Vector3r()
    geo_point = GeoPoint()
    gravity = Vector3r()
    air_pressure = 0.0
    temperature = 0.0
    air_density = 0.0


class CarState(MsgpackMixin):
    speed = 0.0
    gear = 0
    rpm = 0.0
    maxrpm = 0.0
    handbrake = False
    collision = CollisionInfo()
    kinematics_estimated = KinematicsState()
    timestamp = np.uint64(0)


class MultirotorState(MsgpackMixin):
    collision = CollisionInfo()
    kinematics_estimated = KinematicsState()
    gps_location = GeoPoint()
    timestamp = np.uint64(0)
    landed_state = LandedState.Landed
    rc_data = RCData()
    ready = False
    ready_message = ""
    can_arm = False


class RotorStates(MsgpackMixin):
    timestamp = np.uint64(0)
    rotors = []


class ProjectionMatrix(MsgpackMixin):
    matrix = []


class CameraInfo(MsgpackMixin):
    pose = Pose()
    fov = -1
    proj_mat = ProjectionMatrix()


class LidarData(MsgpackMixin):
    """
    Lidar for multirotor and cars in AirGen. Multiple Lidar with different settings can be installed on a vehicle with different Lidar sensor names.


    default settings in settings.json:
    ::

        {
            "DefaultSensors": {
                "LidarSensorName": {
                    "SensorType": 6,
                    "Enabled" : true,
                    "NumberOfChannels": 16, # Number of channels/lasers of the lidar
                    "Range": 10000, # Max distance of the lidar in meters
                    "RotationsPerSecond": 10, # Number of times the lidar rotates per second
                    "PointsPerSecond": 100000, # Number of points captured per second
                    "X": 0, "Y": 0, "Z": -1, # Position of the lidar relative to the vehicle (in NED, in meters)
                    "Roll": 0, "Pitch": 0, "Yaw" : 0, # Orientation of the lidar relative to the vehicle (in degrees, yaw-pitch-roll order to front vector +X)
                    "VerticalFOVUpper": -15, # Vertical FOV upper limit for the lidar, in degrees (multirotor -15, car +10)
                    "VerticalFOVLower": -45, # Vertical FOV lower limit for the lidar, in degrees (multirotor -45, car -10)
                    "HorizontalFOVStart": 0, # Horizontal FOV start for the lidar, in degrees
                    "HorizontalFOVEnd": 359, #Horizontal FOV end for the lidar, in degrees
                    "DrawDebugPoints": true,
                    "DataFrame": "SensorLocalFrame" # Frame for the points in output ("VehicleInertialFrame" or "SensorLocalFrame")
                }
            }
        }

    usage::

    >>> lidar_data=airgen_client.getLidarData("LidarSensorName")
    """

    point_cloud: List[float] = []
    """point cloud data represented by a list of 3d coordinates ([x0,y0,z0,x1,y1,z1...]), len(point_cloud) = 3 * NumberOfPoints"""
    time_stamp = np.uint64(0)
    """timestamp of the lidar data"""
    pose: Pose = Pose()
    """ pose of the lidar sensor"""
    segmentation: List[int] = []
    """Segmentation Id of each point in the point cloud, len(segmentation) = NumberOfPoints"""


class ImuData(MsgpackMixin):
    """
    Imu for multirotor and cars in AirGen.

    default settings in settings.json:
    ::

        {
            "DefaultSensors": {
                "IMUSensorName": {
                    "SensorType": 2,
                    "Enabled" : true,
                    "AngularRandomWalk": 0.3, # TODO: ADD explanation
                    "GyroBiasStabilityTau": 500,
                    "GyroBiasStability": 4.6,
                    "VelocityRandomWalk": 0.24,
                    "AccelBiasStabilityTau": 800,
                    "AccelBiasStability": 36
                }
            }
        }

    usage::

    >>> imu_data=airgen_client.getImuData("IMUSensorName")
    """

    time_stamp = np.uint64(0)
    """timestamp of the imu data"""
    orientation: Quaternionr = Quaternionr()
    """orientation of the imu"""
    angular_velocity: Vector3r = Vector3r()
    """angular velocity of the imu"""
    linear_acceleration: Vector3r = Vector3r()
    """linear acceleration of the imu"""


class BarometerData(MsgpackMixin):
    """
    Barometer for multirotor and cars in AirGen.

    default settings in settings.json:
    ::

        {
            "DefaultSensors": {
                "BarometerSensorName": {
                    "SensorType": 1,
                    "Enabled" : true,
                    "PressureFactorSigma": 0.001825,
                    "PressureFactorTau": 3600,
                    "UncorrelatedNoiseSigma": 2.7,
                    "UpdateLatency": 0,
                    "UpdateFrequency": 50,
                    "StartupDelay": 0
            }
        }

    usage:

    >>> barometer_data=airgen_client.getBarometerData("BarometerSensorName")

    """

    time_stamp: np.uint64 = np.uint64(0)
    """timestamp of the barometer data """
    altitude: Quaternionr = Quaternionr()
    """altitude of the barometer"""
    pressure: Vector3r = Vector3r()
    """pressure of the barometer"""
    qnh: Vector3r = Vector3r()
    """qnh of the barometer"""


class MagnetometerData(MsgpackMixin):
    """
    Magnetometer for multirotor and cars in AirGen.

    default settings in settings.json:

    ::

        {
            "DefaultSensors": {
                "MagnetometerSensorName": {
                    "SensorType": 3, # TODO: ADD explanation"SensorType": 4,
                    "Enabled" : true,
                    "NoiseSigma": 0.005,
                    "ScaleFactor": 1,
                    "NoiseBias": 0,
                    "UpdateLatency": 0,
                    "UpdateFrequency": 50,
                    "StartupDelay": 0
                    }
                }
        }


    usage::

    >>> magnetometer_data=airgen_client.getMagnetometerData("MagnetometerSensorName")
    """

    time_stamp = np.uint64(0)
    """timestamp of the magnetometer data"""
    magnetic_field_body: Vector3r = Vector3r()
    """timestamp of the magnetometer data"""
    magnetic_field_covariance: float = 0.0
    """magnetic field covariance of the magnetometer"""


class GnssFixType(MsgpackMixin):
    """
    Represents the GNSS (Global Navigation Satellite System) fix types in AirGen.

    This class categorizes the various types of GNSS fixes based on the quality and source of satellite data.

    """

    GNSS_FIX_NO_FIX = 0
    GNSS_FIX_TIME_ONLY = 1
    GNSS_FIX_2D_FIX = 2
    GNSS_FIX_3D_FIX = 3


class GnssReport(MsgpackMixin):
    """
    Represents a GNSS (Global Navigation Satellite System) report in AirSim.

    This class provides detailed information about the current GNSS status and readings.

    """

    geo_point = GeoPoint()
    eph = 0.0
    epv = 0.0
    velocity = Vector3r()
    fix_type = GnssFixType()
    time_utc = np.uint64(0)


class GpsData(MsgpackMixin):
    """
    GPS sensor

    default settings in settings.json:
    ::

        {
            "DefaultSensors": {
                "GPSSensorName": {
                    "SensorType": 3,
                    "Enabled" : true,
                    "EphTimeConstant": 0.9,
                    "EpvTimeConstant": 0.9,
                    "EphInitial": 25,
                    "EpvInitial": 25,
                    "EphFinal": 0.1,
                    "EpvFinal": 0.1,
                    "EphMin3d": 3,
                    "EphMin2d": 4,
                    "UpdateLatency": 0.2,
                    "UpdateFrequency": 50,
                    "StartupDelay": 1
                    }
                }
        }


    usage::

    >>> gps_data=airgen_client.getGpsData("GPSSensorName")
    """

    time_stamp = np.uint64(0)
    """timestamp of the gps data"""
    gnss = GnssReport()
    """gnss report of the gps"""
    is_valid = False
    """whether the gps data is valid"""


class DistanceSensorData(MsgpackMixin):
    """
    Distance sensor

    default settings in settings.json:
    ::

        {
            "DefaultSensors": {
                "DistanceSensorName": {
                    "SensorType": 5,
                    "Enabled" : true,
                    "MinDistance": 0.2, # Minimum distance measured by distance sensor (metres, only used to fill Mavlink message for PX4) (Default 0.2m)
                    "MaxDistance": 40, Maximum distance measured by distance sensor (metres) (Default 40.0m)
                    "X": 0, "Y": 0, "Z": -1, # Position of the sensor relative to the vehicle (in NED, in meters) (Default (0,0,0)-Multirotor, (0,0,-1)-Car)
                    "Yaw": 0, "Pitch": 0, "Roll": 0, # Orientation of the sensor relative to the vehicle (degrees) (Default (0,0,0))
                    "ExternalController": false, # Whether the sensor is controlled by an external controller (Default false)Whether data is to be sent to external controller such as ArduPilot or PX4 if being used (default true)
                    "DrawDebugPoints": false
                    }
                }
        }

    Note:
        For Cars, the sensor is placed 1 meter above the vehicle center by default. This is required since otherwise the sensor gives strange data due it being inside the vehicle. This doesn't affect the sensor values say when measuring the distance between 2 cars.

    usage::

    >>> distance_sensor_data=airgen_client.getDistanceSensorData("DistanceSensorName")
    """

    time_stamp = np.uint64(0)
    """ timestamp of the distance sensor data"""
    distance: float = 0.0
    """ distance measured by the distance sensor"""
    min_distance: float = 0.0
    """minimum distance measured by the distance sensor
    """
    max_distance: float = 0.0
    """maximum distance measured by the distance sensor"""
    relative_pose: Pose = Pose()
    """relative pose of the distance sensor """


class Box2D(MsgpackMixin):
    min = Vector2r()
    max = Vector2r()


class Box3D(MsgpackMixin):
    min = Vector3r()
    max = Vector3r()


class DetectionInfo(MsgpackMixin):
    name = ""
    geo_point = GeoPoint()
    box2D = Box2D()
    box3D = Box3D()
    relative_pose = Pose()


class PIDGains:
    """
    Struct to store values of PID gains. Used to transmit controller gain values while instantiating
    AngleLevel/AngleRate/Velocity/PositionControllerGains objects.

    Attributes:
        kP (float): Proportional gain
        kI (float): Integrator gain
        kD (float): Derivative gain
    """

    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def to_list(self):
        return [self.kp, self.ki, self.kd]


class AngleRateControllerGains:
    """
    Struct to contain controller gains used by angle level PID controller

    Attributes:
        roll_gains (PIDGains): kP, kI, kD for roll axis
        pitch_gains (PIDGains): kP, kI, kD for pitch axis
        yaw_gains (PIDGains): kP, kI, kD for yaw axis
    """

    def __init__(
        self,
        roll_gains=PIDGains(0.25, 0, 0),
        pitch_gains=PIDGains(0.25, 0, 0),
        yaw_gains=PIDGains(0.25, 0, 0),
    ):
        self.roll_gains = roll_gains
        self.pitch_gains = pitch_gains
        self.yaw_gains = yaw_gains

    def to_lists(self):
        return (
            [self.roll_gains.kp, self.pitch_gains.kp, self.yaw_gains.kp],
            [self.roll_gains.ki, self.pitch_gains.ki, self.yaw_gains.ki],
            [self.roll_gains.kd, self.pitch_gains.kd, self.yaw_gains.kd],
        )


class AngleLevelControllerGains:
    """
    Struct to contain controller gains used by angle rate PID controller

    Attributes:
        roll_gains (PIDGains): kP, kI, kD for roll axis
        pitch_gains (PIDGains): kP, kI, kD for pitch axis
        yaw_gains (PIDGains): kP, kI, kD for yaw axis
    """

    def __init__(
        self,
        roll_gains=PIDGains(2.5, 0, 0),
        pitch_gains=PIDGains(2.5, 0, 0),
        yaw_gains=PIDGains(2.5, 0, 0),
    ):
        self.roll_gains = roll_gains
        self.pitch_gains = pitch_gains
        self.yaw_gains = yaw_gains

    def to_lists(self):
        return (
            [self.roll_gains.kp, self.pitch_gains.kp, self.yaw_gains.kp],
            [self.roll_gains.ki, self.pitch_gains.ki, self.yaw_gains.ki],
            [self.roll_gains.kd, self.pitch_gains.kd, self.yaw_gains.kd],
        )


class VelocityControllerGains:
    """
    Struct to contain controller gains used by velocity PID controller

    Attributes:
        x_gains (PIDGains): kP, kI, kD for X axis
        y_gains (PIDGains): kP, kI, kD for Y axis
        z_gains (PIDGains): kP, kI, kD for Z axis
    """

    def __init__(
        self,
        x_gains=PIDGains(0.2, 0, 0),
        y_gains=PIDGains(0.2, 0, 0),
        z_gains=PIDGains(2.0, 2.0, 0),
    ):
        self.x_gains = x_gains
        self.y_gains = y_gains
        self.z_gains = z_gains

    def to_lists(self):
        return (
            [self.x_gains.kp, self.y_gains.kp, self.z_gains.kp],
            [self.x_gains.ki, self.y_gains.ki, self.z_gains.ki],
            [self.x_gains.kd, self.y_gains.kd, self.z_gains.kd],
        )


class PositionControllerGains:
    """
    Struct to contain controller gains used by position PID controller

    Attributes:
        x_gains (PIDGains): kP, kI, kD for X axis
        y_gains (PIDGains): kP, kI, kD for Y axis
        z_gains (PIDGains): kP, kI, kD for Z axis
    """

    def __init__(
        self,
        x_gains=PIDGains(0.25, 0, 0),
        y_gains=PIDGains(0.25, 0, 0),
        z_gains=PIDGains(0.25, 0, 0),
    ):
        self.x_gains = x_gains
        self.y_gains = y_gains
        self.z_gains = z_gains

    def to_lists(self):
        return (
            [self.x_gains.kp, self.y_gains.kp, self.z_gains.kp],
            [self.x_gains.ki, self.y_gains.ki, self.z_gains.ki],
            [self.x_gains.kd, self.y_gains.kd, self.z_gains.kd],
        )


class MeshPositionVertexBuffersResponse(MsgpackMixin):
    position = Vector3r()
    orientation = Quaternionr()
    vertices = 0.0
    indices = 0.0
    name = ""

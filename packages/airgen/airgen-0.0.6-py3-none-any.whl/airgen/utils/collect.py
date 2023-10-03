# utils for data collection in AirGen

from typing import Callable, Optional
import threading
import time

from airgen import airgen_logger
from airgen.client import connect_airgen, VehicleClient, MultirotorClient, CarClient


def data_collector(
    data_collection_task: Callable,
    time_delta=1,
    ip_address: str = "",
    port: int = 41451,
):
    """function decorator for collecting data along trajectory

    TODO:
        - [ ] add a way to stop collecting data when it gets too large or too slow

    Args:
        data_collection_task (Callable): user-defined function for reading measurements from airgen simulator. It should be defined in the following form:
            def data_collection_task(client: VehicleClient, ...) -> Dict[str, Any]:
                ...
        time_delta (float, optional): time (seconds) between consecutive data collections. Defaults to 1.
        ip_address (str, optional): ip address to connect to airgen server. Defaults to "" (localhost).

    Usage:

    >>> def task(client: VehicleClient) -> Dict[str, Any]:
    >>>     return {"position": client.getVehiclePose().position}
    >>>
    >>> @data_collector(task, time_delta=1) # collect positiion every one second during moving towards position
    >>> def moveToPosition(client: airgen.MultirotorClient, position: Vector3r):
    >>>     client.moveToPositionAsync(position.x_val, position.y_val, position.z_val, 5).join()
    >>> _, data = moveToPosition(client, Vector3r(1, 2, 3), _collecting_data=True)
    >>> # or if you don't intent to collect data during moving
    >>> moveToPosition(client, Vector3r(1, 2, 3), _collecting_data=False)
    >>> # or simply, if you don't want to collect data at all (_collect_data is False by default)
    >>> moveToPosition(client, Vector3r(1, 2, 3))
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            if not kwargs.get("_collect_data", False):
                return func(*args, **kwargs)

            # conditional varialbe for stopping the thread
            _stopped = threading.Event()
            _data = []

            def data_collection_loop():
                _collector_client: VehicleClient = connect_airgen(
                    robot_type="vehicle",
                    ip_address=ip_address,
                    port=port,
                    run_in_background=True,
                )
                while not _stopped.is_set():
                    _res, _err = None, False
                    try:
                        # todo: this is probably too slow
                        _res = data_collection_task(_collector_client)
                    except Exception as err:
                        _err = True
                        airgen_logger.warning(
                            "error in data collection task: %s, return data collection task:%s, is not complete",
                            str(err),
                            data_collection_task.__name__,
                        )
                    if _err:
                        break

                    _data.append(_res)
                    time.sleep(time_delta)

            thread = threading.Thread(target=data_collection_loop)
            thread.start()

            _result = func(*args, **kwargs)
            # stop the thread
            _stopped.set()
            thread.join()
            return _result, _data

        return wrapper

    return decorator


def collision_collector(
    ip_address: str = "",
    port: int = 41451,
):
    """monitor collision informations along a trajectory

    TODO:
        - [ ] add a way to stop collecting collision info when it gets too large or program gets too slow

    Args:
        ip_address (str, optional): ip address to connect to airgen server. Defaults to "" (localhost).
        port (int, optional): port to connect to airgen server. Defaults to 41451.

    Note:
        - this function decorator only works for multirotor client for now
        - the first argument of the function being decorated must be the multirotor client
        - runtime arguments:
            - __vehicle_name__: name of the vehicle to monitor collision info
            - __stop_at_collision__: whether to stop the vehicle when collision happens, after which the drone hovers
            - __collecting_collision__: whether to collect collision info and return collected collision data. If this is set to True, the function will return a tuple of (original_func_return, collision_data)

    Usage as a function decorator:

    >>> @collision_collector() # monitor and collect collision information while below task is being executed
    >>> def moveToPosition(client: airgen.MultirotorClient, position: Vector3r. **kwargs):
    >>>     client.moveToPositionAsync(position.x_val, position.y_val, position.z_val, 5).join()
    >>> _, data = moveToPosition(client, Vector3r(1, 2, 3), _stop_at_collision=True, _collect_collision=True)
    >>> # the effect of other parameters is pretty self-explanatory
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            _vehicle_name = kwargs.get("_vehicle_name", "")
            _stop_at_collision = kwargs.get("_stop_at_collision", False)
            _collect_collision = kwargs.get("_collect_collision", False)
            if type(args[0]) != MultirotorClient:
                raise ValueError(
                    "collision collector only works for multirotor client for now"
                )
            if (not _stop_at_collision) and (not _collect_collision):
                return func(*args, **kwargs)

            # conditional varialbe for stopping the thread
            _stopped = threading.Event()
            _collision_data = []

            def get_collision_loop():
                _collector_client: VehicleClient = connect_airgen(
                    robot_type="vehicle",
                    ip_address=ip_address,
                    port=port,
                    run_in_background=True,
                )
                _flag = True
                while _flag:
                    if _stopped.is_set():
                        _flag = False
                    collision_info = _collector_client.simGetCollisionInfo(
                        vehicle_name=_vehicle_name
                    )

                    if collision_info.has_collided:
                        if _collect_collision:
                            _collision_data.append(collision_info)
                        if _stop_at_collision:
                            # stop the async task
                            args[0].cancelLastTask(vehicle_name=_vehicle_name)
                            path = args[0].simPlanPathToRandomFreePoint(
                                search_radius=3.0, smooth_path=True, draw_path=False
                            )
                            if len(path) > 0:
                                args[0].moveOnPathAsync(
                                    path, 1.0, vehicle_name=_vehicle_name
                                ).join()
                            args[0].hoverAsync().join()
                            break
                    time.sleep(1)

            thread = threading.Thread(target=get_collision_loop)
            # clear out the collision data
            args[0].simGetCollisionInfo(vehicle_name=_vehicle_name)
            # then starts running both the collision info collector and the original function
            thread.start()
            _result = func(*args, **kwargs)
            # stop the thread
            _stopped.set()
            thread.join()
            if _collect_collision:
                return _result, _collision_data
            return _result

        return wrapper

    return decorator

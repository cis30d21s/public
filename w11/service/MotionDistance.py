from gpiozero import DistanceSensor, MotionSensor
from typing import Callable
import warnings
from gpiozero.exc import DistanceSensorNoEcho
# ignore 'no echo received' warnings
warnings.simplefilter('ignore', DistanceSensorNoEcho)


class MotionDistanceMonitor:
    def __init__(self,
                 motion_pin: int,
                 trigger_pin: int,
                 echo_pin: int,
                 motion_callback: Callable[[float], None],
                 no_motion_callback: Callable[[float], None],
                 armed: Callable[[], bool]):
        self.pir = MotionSensor(motion_pin)
        self.distance_sensor = DistanceSensor(
            trigger=trigger_pin, echo=echo_pin, max_distance=1)
        self.pir.when_motion = lambda: motion_callback(
            self.distance) if armed() else None
        self.pir.when_no_motion = lambda: no_motion_callback(
            self.distance) if armed() else None

    @property
    def distance(self) -> float:
        return self.distance_sensor.distance

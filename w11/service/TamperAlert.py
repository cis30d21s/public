# if sense hat emulator is missing on the pi, install it:
# $ sudo apt install sense-emu-tools
import logging
from typing import Callable
from sense_emu import SenseHat
import threading
import atexit
import time


class TamperAlert:
    def __init__(self, change_percent: float = 0.1, tick: float = 0.01, movement_check_interval: float = 1):
        self.sense = SenseHat()
        # amount of change to be considered movement
        self.change_percent = change_percent
        self.tick = tick  # sampling interval
        self.movement_check_interval = movement_check_interval
        self.orientation = self.sense.get_orientation()
        self._moved_event = threading.Event()
        TamperAlert._stop_event = threading.Event()
        self._moved_thread = threading.Thread(
            target=self._run, name=f'Moved-{threading.active_count()+1}', daemon=True)
        self._moved_thread.start()

    @property
    def when_moved(self) -> Callable[[], None]:
        raise NotImplementedError

    @when_moved.setter
    def when_moved(self, callback: Callable[[], None]):
        if callback:
            self._when_moved = callback
            self._moved_event.set()

    def _run(self):
        self._moved_event.wait()  # wait until callback is set
        tick_counter = 0
        change_counter = 0
        while not TamperAlert._stop_event.is_set():
            tick_counter += 1
            orientation = self.sense.get_orientation()
            if self._changed(orientation['pitch'], self.orientation['pitch']) \
                    or self._changed(orientation['roll'], self.orientation['roll']) \
                    or self._changed(orientation['yaw'], self.orientation['yaw']):
                change_counter += 1
                if change_counter * 2 >= tick_counter:  # changed at least 50% of time
                    change_counter = 0
                    try:
                        self._when_moved()
                    except Exception as e:
                        logging.error(f'Callback failed: {e}')
            if tick_counter >= self.movement_check_interval // self.tick:
                self.orientation = orientation  # new baseline
                tick_counter = 0
                change_counter = 0
            time.sleep(self.tick)

    def _changed(self, value: float, baseline: float) -> bool:
        return abs((value-baseline)/baseline) >= self.change_percent if baseline else False

    @staticmethod
    @atexit.register
    def _stop_threads():
        TamperAlert._stop_event.set()

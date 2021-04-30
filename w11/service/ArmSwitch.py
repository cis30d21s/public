from typing import Callable
from gpiozero import LED, Button


class ArmSwitch:
    def __init__(self, led_pin: int, button_pin: int, callback: Callable[[bool], None]):
        self.led = LED(led_pin)
        self.button = Button(button_pin, bounce_time=0.1)

        def handle_change():
            self.led.toggle()
            callback(self.led.is_active)
        self.button.when_released = handle_change

    @property
    def armed(self) -> bool:
        return self.led.is_active

    @armed.setter
    def armed(self, value: bool):
        self.led.value = value

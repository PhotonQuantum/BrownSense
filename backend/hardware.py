#!/usr/bin/python3
import random


class Sensor:
    _terminated = False

    def __init__(self, sensor_ports=None, dummy=False):
        if sensor_ports is None:
            sensor_ports = [1, 2]
        if dummy:
            self._dummy_data = [50, 50]
        else:
            self._dummy_data = None
            # TODO init sensors here

    def __del__(self):
        print("[-] Sensor terminated")
        self._terminated = True
        # TODO stop sensors

    def stream(self):
        while not self._terminated:
            if self._dummy_data:
                self._dummy_data[0] += random.randint(-3, 3)
                self._dummy_data[1] += random.randint(-3, 3)
                rtn = self._dummy_data
            else:
                # TODO read sensor data here
                rtn = 0
                print("delete this line")
            yield rtn

    @property
    def reading(self):
        if self._dummy_data:
            return self._dummy_data
        else:
            # TODO return sensor data
            return "..."


class Actuator:
    def __init__(self, relay_port=1, dummy=False):
        if dummy:
            self._dummy_status = -1
        else:
            # TODO init relay here
            self._dummy_status = None

    def __del__(self):
        # TODO open relay and stop GPIO
        print("[-] Relay released")

    @property
    def closed(self):
        if self._dummy_status:
            return False if self._dummy_status == -1 else True
        else:
            # TODO read relay status here (GPIO.read(x))
            return False

    @closed.setter
    def closed(self, val):
        if self._dummy_status:
            self._dummy_status = 1 if val else -1
        else:
            # TODO set relay state here
            print("delete me")

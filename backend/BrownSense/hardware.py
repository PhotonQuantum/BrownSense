#!/usr/bin/python3
import random
from loguru import logger
from PiPyADC.pipyadc import ADS1256
from PiPyADC.ADS1256_definitions import POS_AIN0, POS_AIN1, NEG_AINCOM
CH1 = POS_AIN0 | NEG_AINCOM
CH2 = POS_AIN1 | NEG_AINCOM
CH_SEQ = (CH1, CH2)


class Sensor:
    _terminated = False
    _ads = None

    def __init__(self, dummy=False):
        if dummy:
            self._dummy_data = [50, 50]
        else:
            self._dummy_data = None
            self._ads = ADS1256()
            logger.debug("Calibrating ADC")
            self._ads.cal_self()
            logger.info("ADC Ready")

    def __del__(self):
        logger.info("Sensor terminated")
        self._terminated = True
        # TODO stop sensors

    def stream(self):
        while not self._terminated:
            if self._dummy_data:
                self._dummy_data[0] += random.randint(-3, 3)
                self._dummy_data[1] += random.randint(-3, 3)
                rtn = self._dummy_data
            else:
                raw_readings = self._ads.read_sequence(CH_SEQ)
                rtn = [round(i * self._ads.v_per_digit * 100, 2) for i in raw_readings]
            yield rtn

    @property
    def reading(self):
        if self._dummy_data:
            return self._dummy_data
        else:
            raw_readings = self._ads.read_sequence(CH_SEQ)
            rtn = [round(i * self._ads.v_per_digit * 100, 2) for i in raw_readings]
            return rtn
            pass


class Actuator:
    def __init__(self, dummy=False):
        if dummy:
            self._dummy_status = -1
        else:
            # TODO init relay here
            self._dummy_status = None

    def __del__(self):
        # TODO open relay and stop GPIO
        logger.info("Relay released")

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
            pass

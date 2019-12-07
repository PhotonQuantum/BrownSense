#!/usr/bin/python3
from concurrent.futures.thread import ThreadPoolExecutor
import time
from db import Remote
from hardware import Sensor, Actuator
from utils import GracefulKiller, wait_network_online
import config as cfg
from loguru import logger

override = 0


def main():
    killer = GracefulKiller()
    sensor = Sensor(cfg.sensor_ports, cfg.debug_sensor)
    actuator = Actuator(cfg.relay_port, cfg.debug_actuator)
    with ThreadPoolExecutor() as executor, Remote(cfg.couchdb, cfg.device_id, callback, cfg.graceful) as remote:
        executor.submit(report_thread, remote, sensor, actuator, killer)

        sensor_stream = sensor.stream()
        report_counter = 0
        for reading in sensor_stream:
            report_counter += 1
            if report_counter > 10:
                remote.report_datagrid(reading)
                report_counter = 0
            if (reading[0] > cfg.limit["h2s"][1] or reading[1] > cfg.limit["nh3"][1]) or (override == "force_on"):
                actuator.closed = True
            elif (reading[0] < cfg.limit["h2s"][0] and reading[0] < cfg.limit["nh3"][0]) or (override == "force_off"):
                actuator.closed = False
            if killer.kill_now:
                logger.debug("[SIGTERM]")
                break
            time.sleep(1)
    logger.info("Main end")


def callback(event, params):
    if event == "override":
        global override
        override = params


def report_thread(remote, sensor, actuator, killer):
    while not killer.kill_now:
        remote.report_summary(override, sensor.reading, actuator.closed)
        time.sleep(1)
    logger.info("report thread terminated")


if __name__ == "__main__":
    main()

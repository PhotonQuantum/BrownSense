#!/usr/bin/python3
from concurrent.futures.thread import ThreadPoolExecutor
import time
from db import Remote
from hardware import Sensor, Actuator
from utils import GracefulKiller, wait_network_online
import config as cfg
import argparse

override = 0


def main():
    killer = GracefulKiller()
    wait_network_online()
    sensor = Sensor(cfg.sensor_ports, cfg.debug)
    actuator = Actuator(cfg.relay_port, cfg.debug)
    with ThreadPoolExecutor() as executor, Remote(cfg.couchdb, cfg.device_id, callback, cfg.graceful) as remote:
        executor.submit(report_thread, remote, sensor, actuator, killer)

        sensor_stream = sensor.stream()
        report_counter = 0
        for reading in sensor_stream:
            report_counter += 1
            if report_counter > 10:
                remote.report_datagrid(reading)
                report_counter = 0
            if reading[0] > cfg.limit["h2s"][1] or reading[1] > cfg.limit["nh3"][1]:
                actuator.closed = True
            elif reading[0] < cfg.limit["h2s"][0] and reading[0] < cfg.limit["nh3"][0]:
                actuator.closed = False
            if killer.kill_now:
                print("[SIGTERM]")
                break
            time.sleep(1)
    print("[-] Main end")


def callback(event, params):
    if event == "override":
        global override
        override = params[0]


def report_thread(remote, sensor, actuator, killer):
    while not killer.kill_now:
        if override == -1:
            override_status = "force_off"
        elif override == 1:
            override_status = "force_on"
        else:
            override_status = "auto"
        remote.report_summary(override_status, sensor.reading, actuator.closed)
        time.sleep(1)
    print("[-] report thread terminated")


if __name__ == "__main__":
    main()

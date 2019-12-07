#!/usr/bin/python3
device_id = 1
couchdb = {
    "host": "https://brownsense.misaka.center/db",
    "username": "***",
    "password": "***"
}
debug_actuator = True
debug_sensor = True
graceful = True
sensor_ports = [1, 2]
relay_port = 1
limit = {
    "h2s": [40, 60],
    "nh3": [40, 60]
}

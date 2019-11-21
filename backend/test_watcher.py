#!/bin/python
from concurrent.futures.thread import ThreadPoolExecutor
from couchdb import Server
from queue import SimpleQueue
from uuid import uuid4
import time
import random
import sys
import json
from enum import Enum

server = Server("https://brownsense.misaka.center/db")
db_datagrid = server["datagrid"]
db_command = server["command"]
db_summary = server["summary"]
task_queue = SimpleQueue()
device_id = sys.argv[1]
nh3=0
h2s=0
terminated = False
actuator = False
try:
    graceful = True if sys.argv[2] == 1 else False
except IndexError:
    graceful = True


class buffer_params():
    override_status = Enum("overrides", "disabled force_on force_off")
    _tmp_lower = 490
    _tmp_upper = 510
    _tmp_override = override_status.disabled

    def __init__(self):
        self.update()

    def update(self):
        self._lower = self._tmp_lower
        self._upper = self._tmp_upper
        self._override = self._tmp_override

    @property
    def lower(self):
        return self._lower

    @lower.setter
    def set_lower(self, val):
        self._tmp_lower = val

    @property
    def upper(self):
        return self._upper

    @upper.setter
    def set_upper(self, val):
        self._tmp_upper = val

    @property
    def override(self):
        return self._override

    @override.setter
    def set_override(self, val):
        self._tmp_override = val


actuator_params = buffer_params()


def update_doc(db, mango_query, data):
    query = list(db.find(mango_query))
    if query:
        data["_id"] = query[0].id
        data["_rev"] = query[0].rev
    else:
        data["_id"] = uuid4().hex
    db.save(data)

def rtn_dict_dg(type, data):
    doc = {"_id": uuid4().hex, "time": time.time(), "device": device_id,
           "type": type, "data": data}
    return doc


def rtn_dict_summary(status, h2s, nh3, actuator):
    return {"device": device_id, "time": time.time(), "status": status, "h2s": h2s, "nh3": nh3, "actuator": actuator}

def db_watcher():
    while not terminated:
        watcher = db_command.changes(feed="longpoll", timeout=5, include_docs=True)
        params = json.loads(watcher)
        # These parameters won't take affect until buffer_params.update is called.
        buffer_params.lower = params["auto_params"]["lower"]
        buffer_params.upper = params["auto_params"]["upper"]
        buffer_params.override = buffer_params.override_status[params["override"]]

def i2c_watcher(queue):
    global h2s
    global nh3
    i2c_data = 500
    nh3_data = 500
    time_count = 0
    while True:
        if terminated:
            break
        i2c_data += random.randint(-2,
                                   3) if not actuator else random.randint(-8, 0)
        nh3_data += random.randint(-2,
                                   3) if not actuator else random.randint(-8, 0)
        h2s = i2c_data
        nh3 = nh3_data
        print(f"[i2c_watcher] i2c: {i2c_data}")
        if (((i2c_data > actuator_params.upper or nh3_data > actuator_params.upper) and not actuator_params.override == actuator_params.override_status.force_off) or actuator_params.override == actuator_params.override_status.force_on) and not actuator:
            print("[i2c_watcher] event trigger!")
            queue.put({"func": acturator_trigger, "params": [True]})
            print("[i2c_watcher] event triggered")
        if (((i2c_data < actuator_params.lower and nh3_data < actuator_params.lower) and not actuator_params.override == actuator_params.override_status.force_on) or actuator_params.override == actuator_params.override_status.force_off) and actuator:
            print("[i2c_watcher] event trigger!")
            queue.put({"func": acturator_trigger, "params": [False]})
            print("[i2c_watcher] event triggered")
        time_count += 1
        if time_count % 30 == 0:
            print("report sensor data")
            db_datagrid.save(rtn_dict_dg("h2s", i2c_data))
            db_datagrid.save(rtn_dict_dg("nh3", nh3_data))
            time_count = 0
        time.sleep(1)


def params_timer():
    while True:
        if terminated:
            break
        actuator_params.update()
        time.sleep(1)


def report_timer():
    while True:
        if terminated:
            break


        if buffer_params.override == buffer_params.override_status.force_on:
            status = "force_on"
        elif buffer_params.override == buffer_params.override_status.force_off:
            status = "force_off"
        else:
            status = "auto"

        update_doc(db_summary, {"selector": {"device": device_id}}, rtn_dict_summary(status, h2s, nh3, actuator))

        time.sleep(1)


def acturator_trigger(enabled):
    global actuator
    print("starting" if enabled else "stoping")
    time.sleep(0.5)
    actuator = enabled
    db_datagrid.save(rtn_dict_dg("actuator", enabled))
    print("started" if enabled else "stoped")


with ThreadPoolExecutor() as executor:
    db_future = executor.submit(db_watcher)
    i2c_future = executor.submit(i2c_watcher, task_queue)
    reporter_future = executor.submit(report_timer)
    params_future = executor.submit(params_timer)
    print("listening for tasks")
    try:
        while True:
            task = task_queue.get()
            executor.submit(task["func"], *task["params"])
    except KeyboardInterrupt:
        terminated = True
        if graceful:
            update_doc(db_summary, {"selector": {"device": device_id}}, rtn_dict_summary("offline", 0, 0, actuator))

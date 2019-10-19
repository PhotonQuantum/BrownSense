#!/bin/python
from concurrent.futures.thread import ThreadPoolExecutor
from couchdb import Server
from queue import SimpleQueue
import time

server = Server("http://127.0.0.1:5984/")
db = server["test"]
task_queue = SimpleQueue()
device_id = 1
terminated = False


def rtn_dict(type, info):
    doc = {"device": device_id, "type": type,
           "info": info, "time": time.time()}
    return doc


def db_watcher():
    watcher = db.changes(feed="continuous", include_docs=True)
    for line in watcher:
        if terminated:
            break
        print(line)


def i2c_watcher(queue):
    i2c_data = ""
    with open("test", mode="r") as f:
        while True:
            if terminated:
                break
            f.seek(0)
            i2c_data = f.read()
            print(f"[i2c_watcher] i2c: {i2c_data}")
            if i2c_data > "510":
                print("[i2c_watcher] event trigger!")
                queue.put({"func": acturator_trigger, "params": [True]})
                print("[i2c_watcher] event triggered")
            elif i2c_data < "490":
                print("[i2c_watcher] event trigger!")
                queue.put({"func": acturator_trigger, "params": [False]})
                print("[i2c_watcher] event triggered")
            db.save(rtn_dict("sensor", i2c_data))
            time.sleep(1)


def acturator_trigger(enabled):
    print("starting" if enabled else "stoping")
    time.sleep(0.5)
    db.save(rtn_dict("actuator", enabled))
    print("started" if enabled else "stoped")


with ThreadPoolExecutor() as executor:
    db.save(rtn_dict("system", "online"))
    db_future = executor.submit(db_watcher)
    i2c_future = executor.submit(i2c_watcher, task_queue)
    print("listening for tasks")
    try:
        while True:
            task = task_queue.get()
            executor.submit(task["func"], *task["params"])
    except KeyboardInterrupt:
        terminated = True
        db.save(rtn_dict("system", "offline"))

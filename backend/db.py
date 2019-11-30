#!/usr/bin/python3
from cloudant import CouchDB
from concurrent.futures.thread import ThreadPoolExecutor
import requests
from uuid import uuid4
from queue import SimpleQueue
import json
import time


class Remote:
    _terminated = False

    def __init__(self, server, device_id, callback, graceful=True):
        self._db = Database(server["host"], server["username"], server["password"], ["summary", "datagrid", "command"])
        self._device_id = str(device_id)
        self._graceful = graceful
        self._callback = callback
        self._dg_queue = SimpleQueue()
        self._executor = ThreadPoolExecutor()
        self._executor.submit(self._dg_submit_thread, self._dg_queue)
        self._executor.submit(self._cmd_watcher_thread)
        print("[+] remote init complete")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("[.] terminating remote objects")
        if self._graceful:
            self.report_summary("offline", [0, 0], False)
        self._terminated = True
        self._dg_queue.put(None)
        print("[.] remote thread shutdown signal sent")
        self._executor.shutdown()
        print("[-] remote terminated")

    def _dg_submit_thread(self, queue):
        while True:
            doc = queue.get()
            if doc:
                print(f"[G] {doc}")
                try:
                    self._db.dbs["datagrid"].create_document(doc)
                except requests.HTTPError as e:
                    if e.response.status_code == 401:
                        print("UnauthorizedError. Maybe device_id is not a user in db?")
                    elif e.response.status_code == 403:
                        print("ForbiddenError. Wrong device_id.")
                    else:
                        raise
            else:
                print("[-] dg_submit_thread terminated")
                break

    def _cmd_watcher_thread(self):
        while not self._terminated:
            watcher = self._db.dbs["command"].changes(feed="longpoll", timeout=5, include_docs=True)
            params = json.loads(watcher)
            if params["device"] == self._device_id:
                print("[C] callback triggered")
                self._callback(params["param"], params["data"])

    def report_summary(self, status, sensor, actuator):
        doc = {"device": self._device_id, "time": time.time(), "status": status,
               "h2s": sensor[0], "nh3": sensor[1],
               "actuator": actuator}
        print(f"[S] {doc}")
        try:
            self._db.update_doc("summary", {"device": self._device_id}, doc)
        except requests.HTTPError as e:
            if e.response.status_code == 401:
                print("UnauthorizedError. Maybe device_id is not a user in db?")
            elif e.response.status_code == 403:
                print("ForbiddenError. Wrong device_id.")
            else:
                raise

    def report_datagrid(self, sensor):
        doc_1 = {"_id": uuid4().hex, "time": time.time(), "device": self._device_id,
                 "type": "h2s", "data": sensor[0]}
        doc_2 = {"_id": uuid4().hex, "time": time.time(), "device": self._device_id,
                 "type": "nh3", "data": sensor[1]}
        self._dg_queue.put(doc_1)
        self._dg_queue.put(doc_2)


class Database:
    # _delays = [0.5, 0.5, 1, 1, 1]
    _delays = [0.5]
    dbs = {}

    def __init__(self, url, username, password, dbs):
        self._server = CouchDB(username, password, url=url, auto_renew=True, timeout=10, connect=True)
        for db in dbs:
            self.dbs[db] = self._server[db]

    def update_doc(self, db, mango_query, data):
        query = self.dbs[db].get_query_result(mango_query)
        if query[0]:
            doc = self.dbs[db][query[0][0]["_id"]]
            for item in data:
                doc[item] = data[item]
            doc.save()
        else:
            try:
                data["_id"] = uuid4().hex
                self.dbs[db].create_document(data)
            except requests.HTTPError as e:
                raise


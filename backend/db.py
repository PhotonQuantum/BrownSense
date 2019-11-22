#!/usr/bin/python3
from couchdb import Server, Session
from concurrent.futures.thread import ThreadPoolExecutor
from uuid import uuid4
from queue import SimpleQueue
import json
import time


class Remote:
    _terminated = False

    def __init__(self, url, device_id, callback, graceful=True):
        self._db = Database(url, ["summary", "datagrid", "command"])
        self._device_id = device_id
        self._graceful = graceful
        self._callback = callback
        self._dg_queue = SimpleQueue()
        self._executor = ThreadPoolExecutor()
        self._executor.submit(self._dg_submit_thread, self._dg_queue)
        self._executor.submit(self._cmd_watcher_thread)
        print("[+] remote init complete")

    def __del__(self):
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
                self._db.dbs["datagrid"].save(doc)
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
        self._db.update_doc("summary", {"selector": {"device": self._device_id}}, doc)

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

    def __init__(self, url, dbs):
        self._session = Session(timeout=3, retry_delays=self._delays)
        self._server = Server(url, session=self._session)
        for db in dbs:
            self.dbs[db] = self._server[db]

    def update_doc(self, db, mango_query, data):
        query = list(self.dbs[db].find(mango_query))
        if query:
            data["_id"] = query[0].id
            data["_rev"] = query[0].rev
        else:
            data["_id"] = uuid4().hex
        self.dbs[db].save(data)

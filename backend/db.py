#!/usr/bin/python3
from cloudant import CouchDB
from concurrent.futures.thread import ThreadPoolExecutor
import requests
from uuid import uuid4
from queue import SimpleQueue
import time
from loguru import logger


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
        logger.info("Remote init complete")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug("Terminating remote objects")
        if self._graceful:
            self.report_summary("offline", [0, 0], False)
        self._terminated = True
        self._dg_queue.put(None)
        logger.debug("Remote thread shutdown signal sent")
        self._executor.shutdown()
        logger.info("Remote terminated")

    @logger.catch
    def _dg_submit_thread(self, queue):
        while True:
            doc = queue.get()
            if doc:
                logger.debug(f"{doc}")
                try:
                    self._db.dbs["datagrid"].create_document(doc)
                except requests.HTTPError as e:
                    if e.response.status_code == 401:
                        logger.error("UnauthorizedError. Maybe device_id is not a user in db?")
                    elif e.response.status_code == 403:
                        logger.error("ForbiddenError. Wrong device_id.")
                    else:
                        raise
            else:
                logger.debug("dg_submit_thread terminated")
                break

    @logger.catch
    def _cmd_watcher_thread(self):
        query = self._db.dbs["command"].get_query_result({"type": "queue", "device": self._device_id})
        if query[0]:
            queue_top = query[0][0]["top"]
        else:
            queue_top = 0
        while not self._terminated:
            print(f"[C] MQ top: { queue_top }")
            query = self._db.dbs["command"].get_query_result(
                {"type": "task", "device": self._device_id, "created_at": {"$gt": queue_top}}, sort=[{"created_at": "desc"}])
            if query[0]:
                params = query[0][0]
                queue_top = params["created_at"]
                self._db.update_doc("command", {"type": "queue", "device": self._device_id}, {"type": "queue", "device": self._device_id, "top": queue_top})
                self._callback(params["payload"]["event"], params["payload"]["data"])
            time.sleep(1)

    def report_summary(self, status, sensor, actuator):
        doc = {"device": self._device_id, "time": time.time(), "status": status,
               "h2s": sensor[0], "nh3": sensor[1],
               "actuator": actuator}
        logger.debug(f"{doc}")
        try:
            self._db.update_doc("summary", {"device": self._device_id}, doc)
        except requests.HTTPError as e:
            if e.response.status_code == 401:
                logger.error("UnauthorizedError. Maybe device_id is not a user in db?")
            elif e.response.status_code == 403:
                logger.error("ForbiddenError. Wrong device_id.")
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
        # try: except ConnectionError:
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

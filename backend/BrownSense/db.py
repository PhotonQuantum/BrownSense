#!/usr/bin/python3
from cloudant import CouchDB
from concurrent.futures.thread import ThreadPoolExecutor
from requests.exceptions import HTTPError, ConnectionError, Timeout
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
                retry = True
                while retry:
                    try:
                        self._db.datagrid.create_document(doc)
                        retry = False
                    except HTTPError as e:
                        retry = False
                        if e.response.status_code == 401:
                            logger.error("UnauthorizedError. Maybe device_id is not a user in db?")
                        elif e.response.status_code == 403:
                            logger.error("ForbiddenError. Wrong device_id.")
                        else:
                            raise
                    except (ConnectionError, Timeout) as e:
                        logger.warning("Network error.")
                        retry = True
                        time.sleep(1)
                    except Database.DatabaseNotReadyError:
                        logger.warning("Database not ready")
                        retry = True
                        time.sleep(1)
            else:
                logger.debug("dg_submit_thread terminated")
                break

    @logger.catch
    def _cmd_watcher_thread(self):
        retry = True
        while retry:
            try:
                if self._terminated: return
                query = self._db.command.get_query_result({"type": "queue", "device": self._device_id})
                retry = False
            except Database.DatabaseNotReadyError:
                logger.debug("Database not ready, waiting...")
                time.sleep(1)

        logger.info("MQ started.")

        if query[0]:
            queue_top = query[0][0]["top"]
        else:
            queue_top = 0
        while not self._terminated:
            query = self._db.command.get_query_result(
                {"type": "task", "device": self._device_id, "created_at": {"$gt": queue_top}}, sort=[{"created_at": "desc"}])
            try:
                query_result = query[0]
            except (ConnectionError, Timeout) as e:
                logger.warning("MQ lost.")
                query_result = None
            if query_result:
                params = query_result[0]
                logger.info(f"{ params }")
                self._callback(params["payload"]["event"], params["payload"]["data"])
                queue_top = params["created_at"]
                retry = True
                while retry:
                    try:
                        if self._terminated: return
                        self._db.update_doc("command", {"type": "queue", "device": self._device_id}, {"type": "queue", "device": self._device_id, "top": queue_top})
                        logger.debug(f"MQ top updated")
                        retry = False
                    except (ConnectionError, Timeout) as e:
                        logger.warning("Network error")
                        time.sleep(1)

            time.sleep(1)

    def report_summary(self, status, sensor, actuator):
        doc = {"device": self._device_id, "time": time.time(), "status": status,
               "h2s": sensor[0], "nh3": sensor[1],
               "actuator": actuator}
        logger.debug(f"{doc}")
        try:
            self._db.update_doc("summary", {"device": self._device_id}, doc)
        except HTTPError as e:
            if e.response.status_code == 401:
                logger.error("UnauthorizedError. Maybe device_id is not a user in db?")
            elif e.response.status_code == 403:
                logger.error("ForbiddenError. Wrong device_id.")
            elif e.response.status_code == 409:
                logger.error("Conflict. Slow network (your last request has reached the server but the client doesn't know) or another device is using the same credential.")
            else:
                raise
        except (ConnectionError, Timeout) as e:
            logger.warning("Network error.")
        except Database.DatabaseNotReadyError:
            logger.warning("Database not ready.")

    def report_datagrid(self, sensor, graph):
        doc_1 = {"_id": uuid4().hex, "time": time.time(), "device": self._device_id,
                 "type": "h2s", "data": sensor[0], "graph": graph}
        doc_2 = {"_id": uuid4().hex, "time": time.time(), "device": self._device_id,
                 "type": "nh3", "data": sensor[1], "graph": graph}
        self._dg_queue.put(doc_1)
        self._dg_queue.put(doc_2)


class Database:
    # _delays = [0.5, 0.5, 1, 1, 1]
    _delays = [0.5]
    _dbs = {}
    _connected = False

    class DatabaseNotReadyError(Exception):
        pass

    def __init__(self, url, username, password, dbs):
        self._server = CouchDB(username, password, url=url, auto_renew=True, timeout=10)
        try:
            self._server.connect()
            _connected = True
        except ConnectionError:
            logger.warning("Unable to connect database. Retry at next db call.")
        for db in dbs:
            if self._connected:
                self._dbs[db] = self._server[db]
            else:
                self._dbs[db] = None

    def __getattr__(self, item):
        if item in self._dbs.keys():
            if not self._connected:
                try:
                    self._server.connect()
                    self._connected = True
                except ConnectionError:
                    raise self.DatabaseNotReadyError("Database not connected.")
            if self._dbs[item] is None:
                self._dbs[item] = self._server[item]
            return self._dbs[item]
        else:
            raise AttributeError

    def update_doc(self, db, mango_query, data):
        query = getattr(self, db).get_query_result(mango_query)
        if query[0]:
            doc = getattr(self, db)[query[0][0]["_id"]]
            for item in data:
                doc[item] = data[item]
            doc.save()
        else:
            data["_id"] = uuid4().hex
            getattr(self, db).create_document(data)

#!/usr/bin/python3
import requests
import time
import signal


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


def wait_network_online():
    retry_count = 0
    while True:
        try:
            req = requests.get("http://example.com", timeout=5)
            req.raise_for_status()
            return
        except (requests.HTTPError, requests.ConnectionError) as e:
            retry_count += 1
            if retry_count > 20:
                time.sleep(10)
            elif retry_count > 20:
                time.sleep(5)
            elif retry_count > 10:
                time.sleep(3)
            else:
                time.sleep(1)

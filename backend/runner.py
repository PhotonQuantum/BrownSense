#!/bin/python
import time
import random
with open("test", mode="w") as f:
    density = 500
    while True:
        density += random.randint(-3, 3)
        f.seek(0)
        f.write(str(density))
        f.flush()
        time.sleep(1)


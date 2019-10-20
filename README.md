# BrownSense

🚽 A distributed IoT platform for monitoring and improving toilet's indoor air quality. 

> Work In Progress

0. Deploy Couchdb and create database "test" (serves at http://localhost:5984/)

1. Start dummy data generator
``` bash
cd backend
python runner.py
```

2. Start data backend
``` bash
cd backend
python test_watcher.py
```

3. Serve frontend & hot reload
``` bash
yarn serve
```

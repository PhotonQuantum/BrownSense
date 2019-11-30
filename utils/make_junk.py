#!/usr/bin/python3
from cloudant import CouchDB
import itertools
import sys
server = CouchDB(sys.argv[1], sys.argv[2], url="https://brownsense.misaka.center/db/", connect=True)
db = server["datagrid"]
junk_doc = list(itertools.repeat({"device": "junk_device", "data": "uhaaaaaaaaaaa1145141919810"}, 100))
for i in range(50):
    db.bulk_docs(junk_doc)
    print(i)

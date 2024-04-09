import os

indexdir = "/home/abc7223/app/indexdir"
DBDIR =    "/home/abc7223/app/db.json"

if not os.path.exists(indexdir):
    os.mkdir(indexdir)
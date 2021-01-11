#!/usr/bin/python3

import os
import glob
from datetime import date
from pathlib import Path

class DbFactory:
    def __init__(self):
        d1 = date.today()
        self.today = d1.strftime("%Y-%m-%d")
        self.dbdir = "/media/pi/IMAGEHUB/imagehub_data/db"

    def check_for_dbdir(self):
        if os.path.isdir(self.dbdir):
            if os.path.exists(self.dbdir):
                return True
            else:
                return False

    def current_db_name(self):
        s = self.dbdir + "/*.db"
        dbs = glob.glob(s)
        if len(dbs) < 1:
            return None
        elif len(dbs) == 1:
            return dbs[0]
        else:
            dbs.reverse()
            return dbs[0]

    def dbsize(self):
        s = self.dbdir + "/*.db"
        dbs = glob.glob(s)
        ldbs = len(dbs)
        if ldbs < 1:
            return 0
        elif ldbs == 1:
            statinfo = os.stat(dbs[0])
            size_in_bytes = statinfo.st_size
            size = size_in_bytes/(1024*1024)
            size = str(size)
            return "{}MB".format(size[:5])
        else:
            i = ldbs - 1
            cur_db = dbs[i:]
            statinfo = os.stat(cur_db[0])
            size_in_bytes = statinfo.st_size
            size = size_in_bytes/(1024*1024)
            size = str(size)
            return "{}MB".format(size[:5])

    def stale_db_check(self):
        cdbn = self.current_db_name()
        todaydb = self.today + ".db"
        if cdbn == None:
            return todaydb
        elif cdbn != None:
            if todaydb != cdbn:
                return todaydb
        else:
            return cdbn

    def create(self):
        # if not self.check_for_dbdir():
        #     os.mkdir(self.dbdir)
        cur_db = self.stale_db_check()
        new_dbname = self.dbdir + "/" + cur_db
        Path(new_dbname).touch()
        return new_dbname

if __name__ == '__main__' :
    dbf = DbFactory()
    foo = dbf.create()
    print(foo)
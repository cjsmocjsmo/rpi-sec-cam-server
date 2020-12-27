#!/usr/bin/python3

import os
import glob
from datetime import date
# from pathlib import Path

class DbFactory:
    def __init__(self):
        d1 = date.today()
        self.today = d1.strftime("%d-%m-%Y")
        self.dbdir = "/media/pi/USB31FD/imagehub.db/db"

        # Path('my_file.txt').touch()

    def check_for_dbdir(self):
        if os.path.isdir(self.dbdir):
            if os.path.exists(self.dbdir):
                return True
            else:
                return False

    def current_db_name(self):
        s = self.dbdir + "/*.db"
        dbs = glob.glob(s)
        if len(s) != 0:
            s.reverse()
            return s[0]
        else:
            return None

    def stale_db_check(self):
        cdn = self.current_db_name()
        if cdn != None:
            if self.today != cdn:
                return self.today + ".db"
            else:
                return cdn


    def create(self):
        if not check_for_dbdir():
            os.mkdir(self.dbdir)
        cur_db = current_db_name()
        if cur_db == None:
            new_dbname = self.dbdir + self.today + ".db"
            return new_dbname
        else:
            return self.stale_db_check()





if __name__ == '__main__' :
    dbf = DbFactory()
    dbf.create()
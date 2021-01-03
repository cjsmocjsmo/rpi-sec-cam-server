#!/usr/bin/python3

import os
import yaml
import sqlite3
import dbfactory

y = "/home/pi/imagehub_db_service/secCam.yaml"
with open(y) as f:
    conf = yaml.load(f)[0]

dbname = dbfactory.DbFactory().create()
con = sqlite3.connect(dbname)

class SqlStuff:
    def get_ten_records(self):
        cur = con.cursor()
        cur.execute("SELECT Date Time FROM SecCams")
        zoo = cur.fetchall()
        for z in zoo:
            print(z)

if __name__ == '__main__' :
    ss = SqlStuff()
    ss.get_ten_records()
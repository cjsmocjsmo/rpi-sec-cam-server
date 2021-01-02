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
cur = con.cursor()
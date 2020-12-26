#!/usr/bin/python3

import os
import glob
import base64
import string
import sqlite3
from pprint import pprint

con = sqlite3.connect("imagehub.db")
cur = con.cursor()

foo = cur.execute("SELECT * FROM SecCams")

for f in foo:
    pprint(f)
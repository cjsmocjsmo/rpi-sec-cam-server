#!/usr/bin/python3

import os
import glob
import time
import base64
import string
import sqlite3
import shutil
from pprint import pprint
import dbfactory
import yaml

y = "/home/pi/imagehub_db_service/secCam.yaml"
with open(y) as f:
    conf = yaml.load(f)[0]

dbname = dbfactory.DbFactory().create()
con = sqlite3.connect(dbname)
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS SecCams (Dir text,
            Ext text, Prefix text, Name text, Camera text, Date integer,
            Time text, B64Image text)''')
cur.execute('''CREATE UNIQUE INDEX IF NOT EXISTS TimeIndex ON SecCams (Time)''')

class ProcessSecCamPics:
    def __init__(self):

        self.picdir = conf["image_dir"]
        self.dbdir = conf["db_dir"]

    def get_dir_names(self):
        pic_dir_glob_path = self.picdir + "/*"
        return glob.glob(pic_dir_glob_path)


    def create_b64_image(self, location):
        try:	
            with open(location, 'rb') as imagefile:
                return ''.join(('data:image/png;base64,', base64.b64encode(imagefile.read()).decode('utf-8')))
        except FileNotFoundError:
            print("get_b64_image error")
            print(location)
            return "None"

    def chop_name(self, p, b64image):
        dir, ext = os.path.splitext(p)
        prefix, name = os.path.split(dir)
        rawDate, rawTime = name.split("T", 1)
        camera, dAte = rawDate.split("-", 1)
        timE = str(rawTime)
        # hr, min, sec, ms = rawTime.split(".", 3)
        # x  = (
        #     dirt, ext, prefix, name, camera,
        #     dAte, hr, min, sec, ms, b64image,
        # )
        return (
            dir, ext, prefix, name, camera, dAte, timE, b64image,
        )

    def main(self):
        while True:
            time.sleep(300) #210 3.5 minutes
            dnames = self.get_dir_names()
            for dd in dnames:
                print(dd)
                newname = dd + "/*jpg"
                picglob = glob.glob(newname)
                y = []
                for p in picglob:
                    b64image = self.create_b64_image(p)
                    y.append(self.chop_name(p, b64image))
                    # os.remove(p)
                cur.executemany('''INSERT INTO SecCams VALUES (?,?,?,?,?,?,?,?)''', y)
                con.commit()
                # shutil.rmtree(dd)
            # print("Db insertion complete")



if __name__ == '__main__' :
    PSCP = ProcessSecCamPics()
    PSCP.main()

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

dbname = dbfactory.DbFactory().create()
con = sqlite3.connect(dbname)
# con = sqlite3.connect("/media/pi/USB31FD/imagehub.db")
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS SecCams (Dir text,
            Ext text, Prefix text, Name text, Camera text, Date integer,
            Time integer, B64Image text)''')
cur.execute('''CREATE UNIQUE INDEX IF NOT EXISTS TimeIndex ON Time''')

class ProcessSecCamPics:
    def __init__(self):
        with open('secCam.yaml') as f:
            # conf = yaml.load(f, Loader=yaml.FullLoader)[0]
            conf = yaml.load(f)[0]
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
        # hr, min, sec, ms = rawTime.split(".", 3)
        # x  = (
        #     dirt, ext, prefix, name, camera,
        #     dAte, hr, min, sec, ms, b64image,
        # )
        x  = (
            dir, ext, prefix, name, camera,
            dAte, rawTime, b64image,
        )
        return x

    def main(self):
        while True:
            time.sleep(210) # 3.5 minutes
            y = []
            dnames = self.get_dir_names()
            for dd in dnames:
                newname = dd + "/*jpg"
                picglob = glob.glob(newname)
                for p in picglob:
                    b64image = self.create_b64_image(p)
                    y.append(self.chop_name(p, b64image))
                    os.remove(p)
                cur.executemany('''INSERT INTO SecCams VALUES (?,?,?,?,?,?,?,?)''', y)
                con.commit()
                pprint(y)
                # shutil.rmtree(dd)


    # if __name__ == '__main__' :
#     PSCP = ProcessSecCamPics()
#     while True:
#         time.sleep(300)
#         PSCP.main()
        
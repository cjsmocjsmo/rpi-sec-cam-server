#!/usr/bin/python3

import os
import glob
import time
import base64
import string
import sqlite3
import shutil
from pprint import pprint
import dbfactory as dbfactory
import yaml
import datetime
from pyimagesearch.tempimage import TempImage


y = "/home/pi/imagehub_db_service/secCam.yaml"
with open(y) as f:
    conf = yaml.load(f)[0]

dbname = dbfactory.DbFactory().create()
con = sqlite3.connect(dbname)
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS SecCams (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Dir TEXT,
    Ext TEXT,
    Prefix TEXT,
    Name TEXT,
    Camera TEXT,
    Date integer,
    Time TEXT,
    Picture BLOB);''')
cur.execute('''CREATE UNIQUE INDEX IF NOT EXISTS TimeIndex ON SecCams (Time)''')
client = None

class ProcessSecCamPics:
    def __init__(self):
        if conf["use_dropbox"]:
            #connect to dropbox and start the session authorization process
            self.client = dropbox.Dropbox(conf["dropbox_access_token"])
            print("[SUCCESS] dropbox account linked")

        # self.picdir = conf["image_dir"]
        # self.dbdir = conf["db_dir"]

    # def get_dir_names(self):
    #     pic_dir_glob_path = self.picdir + "/*"
    #     return glob.glob(pic_dir_glob_path)


    # def create_b64_image(self, location):
    #     try:	
    #         with open(location, 'rb') as imagefile:
    #             return ''.join(('data:image/png;base64,', base64.b64encode(imagefile.read()).decode('utf-8')))
    #     except FileNotFoundError:
    #         print("get_b64_image error")
    #         print(location)
    #         return "None"

    def chop_name(self, fname, data):
        dir, ext = os.path.splitext(fname)
        prefix, name = os.path.split(dir)
        rawDate, rawTime = name.split("T", 1)
        camera, dAte = rawDate.split("-", 1)
        timE = str(rawTime)
        return (
            dir, ext, prefix, name, camera, dAte, timE, sqlite3.Binary(data),
        )

    def send_to_dropbox(self, picname, picdata):
        
        # if conf["use_dropbox"]:
        #     #connect to dropbox and start the session authorization process
        #     client = dropbox.Dropbox(conf["dropbox_access_token"])
        #     print("[SUCCESS] dropbox account linked")

        timestamp = datetime.datetime.now()
        ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
        # t = TempImage()
        # with open(picname, "rb") as f:
        #     f.write(t.path, picdata)

        
        path = "/{base_path}/{timestamp}.jpg".format(
            base_path=conf["dropbox_base_path"], timestamp=ts)
        # client.files_upload(open(t.path, "rb").read(), path)


        client.files_upload(open(picdata, "rb").read(), path)
    def main(self, fname, data):

        # while True:
            # dnames = self.get_dir_names()
            # for dd in dnames:
            #     print(dd)
            #     newname = dd + "/*jpg"
            #     picglob = glob.glob(newname)
        y = []
            #     for p in picglob:
        self.send_to_dropbox(fname, data)
        # b64image = self.create_b64_image(p)
        y.append(self.chop_name(fname, data))
        # os.remove(p)
        cur.executemany('''INSERT INTO SecCams VALUES (?,?,?,?,?,?,?,?)''', y)
        con.commit()
                # shutil.rmtree(dd)
            # print("Db insertion complete")
            # time.sleep(3600) # runs initially then sleeps for an hour


# if __name__ == '__main__' :
#     PSCP = ProcessSecCamPics()
#     PSCP.main()

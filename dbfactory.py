#!/usr/bin/python3

import os
import glob
import utils
import sqlite3
import inference as Infer
# import dbfactory
from datetime import date
from pathlib import Path

class DbFactory:
    def __init__(self):
        d1 = date.today()
        self.today = d1.strftime("%Y-%m-%d")
        self.dbdir = "/media/pi/IMAGEHUB/imagehub_data/db"

    def dbsize(self):
        s = self.dbdir + "/*.db"
        dbs = glob.glob(s)
        ldbs = len(dbs)
        if ldbs < 1:
            return "0MB"
        elif ldbs == 1:
            statinfo = os.stat(dbs[0])
            size_in_bytes = statinfo.st_size
            size = size_in_bytes/(1024*1024)
            size = str(size)
            return "{}MB".format(size[:5])
        else:
            i = ldbs - 1
            pc1_cur_db = dbs[i:]
            statinfo = os.stat(pc1_cur_db[0])
            size_in_bytes = statinfo.st_size
            size = size_in_bytes/(1024*1024)
            size = str(size)
            return "{}MB".format(size[:5])
    
    def check_for_dbdir(self):
        if os.path.isdir(self.dbdir):
            if os.path.exists(self.dbdir):
                return True
            else:
                return False

    def pc2_cur_db_name(self):
        pc2 = self.dbdir + "/PiCam2*.db"
        pc2_dbs = glob.glob(pc2)
        len_pc2_dbs = len(pc2_dbs)
        pc2_last = len_pc2_dbs - 1
        pc2_results = None
        if len_pc2_dbs < 1:
            pc2_results = None
        elif len_pc2_dbs == 1:
            pc2_results = pc2_dbs[0]
        else:
            pc2_results = pc2_dbs[pc2_last:]
        return pc2_results

    def pc1_cur_db_name(self):
        pc1 = self.dbdir + "/PiCam1*.db"
        pc1_dbs = glob.glob(pc1)
        len_pc1_dbs = len(pc1_dbs)
        pc1_last = len_pc1_dbs - 1
        pc1_results = None
        if len_pc1_dbs < 1:
            pc1_results = None
        elif len_pc1_dbs == 1:
            pc1_results = pc1_dbs[0]
        else:
            pc1_results = pc1_dbs[pc1_last:]
        return pc1_results



    def pc1_stale_db_check(self):
        cdbn = self.pc1_cur_db_name()
        todaydb = "PiCam1-" + self.today + ".db"
        pc1 = None
        if cdbn == None:
            pc1 = todaydb
        elif cdbn != None:
            if todaydb != cdbn:
                pc1 = todaydb
        else:
            pc1 = cdbn
        return pc1

    def pc2_stale_db_check(self):
        cdbn = self.pc2_cur_db_name()
        todaydb = "PiCam2-" + self.today + ".db"
        pc2 = None
        if cdbn == None:
            pc2 = todaydb
        elif cdbn != None:
            if todaydb != cdbn:
                pc2 = todaydb
        else:
            pc2 = cdbn
        return pc2


    def pc1_create_db(self):
        if not self.check_for_dbdir():
            os.mkdir(self.dbdir)
        cur_db = self.pc1_stale_db_check()
        new_dbname = self.dbdir + "/" + cur_db
        Path(new_dbname).touch()
        return new_dbname

    def pc2_create_db(self):
        if not self.check_for_dbdir():
            os.mkdir(self.dbdir)
        cur_db = self.pc2_stale_db_check()
        new_dbname = self.dbdir + "/" + cur_db
        Path(new_dbname).touch()
        return new_dbname


class PiCam1Sql:
    def create_picam1_db(self):
        dbname = DbFactory().pc1_create_db()
        con = sqlite3.connect(dbname)
        cur = con.cursor()
        # ID INTEGER PRIMARY KEY AUTOINCREMENT,
        cur.execute('''CREATE TABLE IF NOT EXISTS PiCam1DB (
            Dir TEXT,
            Ext TEXT,
            Prefix TEXT,
            Name TEXT,
            Camera TEXT,
            Date integer,
            Time TEXT,
            Picture BLOB);''')
        cur.execute('''CREATE UNIQUE INDEX IF NOT EXISTS TimeIndex ON PiCam1DB (Time)''')
        return dbname

    def chop_name(self, fname):
        dir, ext = os.path.splitext(fname)
        prefix, name = os.path.split(dir)
        rawDate, rawTime = name.split("T", 1)
        camera, dAte = rawDate.split("-", 1)
        timE = str(rawTime)
        imageData = utils.image_data(fname)
        return (dir,
            ext, prefix, name, 
            camera, dAte, timE, 
            sqlite3.Binary(imageData),
        )

    def picam1_db_insert(self, fname_list):
        dbname = self.create_picam1_db()
        # dbname = DbFactory().current_db_name()
        con = sqlite3.connect(dbname)
        cur = con.cursor()
        len_fname_list = len(fname_list)

        for fname in fname_list:
            y = self.chop_name(fname)
            try:
                cur.executemany('''INSERT INTO PiCam1DB VALUES (?,?,?,?,?,?,?,?)''', [y])
                con.commit()
            except sqlite3.IntegrityError:
                pass
        cur.close()
        return len_fname_list

class PiCam2Sql:
    def create_picam2_db(self):
        dbname = DbFactory().pc2_create_db()
        con = sqlite3.connect(dbname)
        cur = con.cursor()
        # ID INTEGER PRIMARY KEY AUTOINCREMENT,
        cur.execute('''CREATE TABLE IF NOT EXISTS PiCam2DB (
            Dir TEXT,
            Ext TEXT,
            Prefix TEXT,
            Name TEXT,
            Camera TEXT,
            Date integer,
            Time TEXT,
            GDStatus TEXT,
            GDProb TEXT,
            GDElpsTime TEXT,
            GMStatus TEXT,
            GMProb TEXT,
            GMElpsTime TEXT,
            PEPStatus TEXT,
            PEPProb TEXT,
            PEPElpsTime TEXT,
            Picture BLOB);''')
        cur.execute('''CREATE UNIQUE INDEX IF NOT EXISTS TimeIndex ON PiCam2DB (Time)''')
        return dbname[1]

    def chop_name(self, fname):
        dir, ext = os.path.splitext(fname)
        prefix, name = os.path.split(dir)
        rawDate, rawTime = name.split("T", 1)
        camera, dAte = rawDate.split("-", 1)
        timE = str(rawTime)
        imageData = utils.image_data(fname)
        gdelpsTime, gdstat, gdprob = Infer.GDClassify([fname])
        gmelpsTime, gmstat, gmprob = Infer.GMClassify([fname])
        pepelpsTime, pepstat, pepprob = Infer.PeopleClassify([fname])
        return (dir,
            ext, prefix, name, 
            camera, dAte, timE,
            gdstat, gdprob, gdelpsTime, 
            gmstat, gmprob, gmelpsTime, 
            pepstat, pepprob, pepelpsTime, 
            sqlite3.Binary(imageData),
        )

    def picam2_db_insert(self, fname_list):
        dbname = self.create_picam2_db()
        con = sqlite3.connect(dbname)
        cur = con.cursor()

        for fname in fname_list:
            y = self.chop_name(fname)
            try:
                cur.executemany('''INSERT INTO PiCam2DB VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', [y])
                con.commit()
            except sqlite3.IntegrityError:
                pass
            # print(y[7], y[8], y[10], y[11], y[13], y[14])
            return y[7], y[8], y[10], y[11], y[13], y[14]
        cur.close()

# if __name__ == '__main__' :
#     dbf = DbFactory()
#     foo = dbf.create()
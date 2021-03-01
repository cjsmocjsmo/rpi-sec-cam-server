#!/usr/bin/python3

import os
import yaml
import uuid
import glob
from pathlib import Path
import io
import sqlite3
# import shutil
import dbfactory
from PIL import Image
from datetime import date
# y = "/home/pi/imagehub_db_service/secCam.yaml"
# with open(y) as f:
#     conf = yaml.load(f)[0]

dbname = dbfactory.DbFactory().current_db_name()
print(dbname)
con = sqlite3.connect(dbname[0])

class SecCamSql:
    def total_log_events(self):
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM SecCamLogs;")
        a = cur.fetchone()
        cur.close()
        return a[0]

    def total_pc1_events(self):
        cur = con.cursor()
        cur.execute("SELECT * FROM SecCamLogs WHERE Body='PiCam1';")
        b = cur.fetchall()
        cur.close()
        return len(b)


    def total_pc2_events(self):
        cur = con.cursor()
        cur.execute("""SELECT * FROM SecCamLogs WHERE Body='PiCam2';""")
        c = cur.fetchall()
        cur.close()
        return len(c)

    def total_health_checks(self):
        cur = con.cursor()
        cur.execute("""SELECT * FROM SecCamLogs WHERE Message='No messages received for 60 minutes';""")
        health_checks = cur.fetchall()
        cur.close()
        if len(health_checks) == 0:
            return "None"
        else:
            return health_checks[0]

        
        


#         self.upload = re.compile("Request to files/upload")

class Pc1Sql:
    def __init__(self):
        # self.tmp_dir = "/tmp/SecCams/SEC"
        # self.tmp_dir_glob = "/tmp/SecCams/SEC/*.jpg"

        self.tmp_dir = "/media/pi/IMAGEHUB/imagehub_data/images/tmp"
        self.tmp_dir_glob = "/media/pi/IMAGEHUB/imagehub_data/images/tmp/*.jpg"
        # mpath = "/media/pi/IMAGEHUB/imagehub_data/images/"

    def pc1_log_last_moving(self):
        try:
            cur = con.cursor()
            cur.execute("""SELECT FullDate FROM SecCamLogs WHERE Body='PiCam1' AND Tail='moving' ORDER BY FullDate ASC LIMIT 1;""")
            z = cur.fetchone()
            cur.close()
            return z[0]
        except TypeError:
            return "No pc1 last_moving present"

    def pc1_log_last_still(self):
        try:
            cur = con.cursor()
            cur.execute("""SELECT FullDate FROM SecCamLogs WHERE Body='PiCam1' AND Tail='still' ORDER BY FullDate ASC LIMIT 1;""")
            x = cur.fetchone()
            cur.close()
            return x[0]
        except TypeError:
            return "No pc2 last_still"

    def clean_tmp_dir(self):
        pa = Path(self.tmp_dir)
        if pa.is_dir():
            if pa.exists():
                tmp_dir_glob_path = "/".join((self.tmp_dir, '*.jpg'))
                tmp_dir_glob = glob.glob(tmp_dir_glob_path)
                for tmp_file in tmp_dir_glob:
                    os.remove(tmp_file)
        else:
            os.mkdir(self.tmp_dir)

            

    def pc1_last25_pics(self):
        self.clean_tmp_dir()
        # g_glob = glob.glob(self.tmp_dir_glob)
        # print("this is g_glob {}".format(g_glob))

        new_pic_list = []
        # if len(g_glob) == 0:
        #     return new_pic_list
        # else:
        cur = con.cursor()
        # cur.execute("""SELECT * FROM SecCams LIMIT 25;""")
        cur.execute("""SELECT * FROM SecCams WHERE Camera='PiCam1' LIMIT 25;""")
        event_list = cur.fetchall()


        print("this is event_list {}".format(event_list))
        for event in event_list:

            print("this is event{}".format(event))
            td = date.today()
            today = td.strftime("%Y-%m-%d")
            tmp_file_n = ".".join((uuid.uuid4().hex, "jpg"))
            tmp_file_name = "-".join((today, tmp_file_n))
            tmp_full_path = "/".join((self.tmp_dir, tmp_file_name))
            with open(tmp_full_path, "wb") as outfile:
                outfile.write(event[13])
            
            new_pic_list.append(tmp_full_path)
        cur.close()
        return new_pic_list


class Pc2Sql:
    def pc2_log_last_moving(self):
        try:
            cur = con.cursor()
            cur.execute("""SELECT Tail FROM SecCamLogs WHERE Body='PiCam2' AND Tail='moving' ORDER BY FullDate ASC LIMIT 1;""")
            z = cur.fetchone()
            cur.close()
            return z[0]
        except TypeError:
            return "No pc2 last moving"

    def pc2_log_last_still(self):
        try:
            cur = con.cursor()
            cur.execute("""SELECT Tail FROM SecCamLogs WHERE Body='PiCam2' AND Tail='still' ORDER BY FullDate ASC LIMIT 1;""")
            x = cur.fetchone()
            cur.close()
            return x[0]
        except TypeError:
            return "No pc2 last_still"







    # def pc1_all_date(self):
    #     cur = con.cursor()
    #     cur.execute("SELECT Date FROM SecCams")
    #     zoo = cur.fetchall()
    #     return zoo

    # def pc1_all_date_time(self):
    #     cur = con.cursor()
    #     cur.execute("SELECT Date, Time FROM SecCams")
    #     zoo = cur.fetchall()
    #     return zoo

    # def pc1_all_date_time_gdstatus(self):
    #     cur = con.cursor()
    #     cur.execute("SELECT Date, Time, GDStatus FROM SecCams")
    #     zoo = cur.fetchall()
    #     return zoo





    # def pc2_all_date(self):
    #     cur = con.cursor()
    #     cur.execute("SELECT Date FROM SecCams")
    #     zoo = cur.fetchall()
    #     return zoo

    # def pc2_all_date_time(self):
    #     cur = con.cursor()
    #     cur.execute("SELECT Date, Time FROM SecCams")
    #     zoo = cur.fetchall()
    #     return zoo

    # def pc2_all_date_time_gdstatus(self):
    #     cur = con.cursor()
    #     cur.execute("SELECT Date, Time, GDStatus FROM SecCams")
    #     zoo = cur.fetchall()
    #     return zoo
        

# if __name__ == '__main__' :
#     ss = SqlStuff()
#     ss.get_ten_records()
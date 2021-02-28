#!/usr/bin/python3

import os
import yaml
import uuid
import glob
import sqlite3
import shutil
import dbfactory
from PIL import Image

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
        self.tmp_dir = "/tmp/SecCams"
        self.tmp_dir_glob = "/tmp/SecCams/*.jpg"

    def pc1_log_last_moving(self):
        cur = con.cursor()
        cur.execute("""SELECT FullDate FROM SecCamLogs WHERE Body='PiCam1' AND Tail='moving' ORDER BY FullDate ASC LIMIT 1;""")
        z = cur.fetchone()
        cur.close()
        if len(z) != 0:
            return z[0]
        else:
            return z

    def pc1_log_last_still(self):
        cur = con.cursor()
        cur.execute("""SELECT FullDate FROM SecCamLogs WHERE Body='PiCam1' AND Tail='still' ORDER BY FullDate ASC LIMIT 1;""")
        x = cur.fetchone()
        cur.close()
        return x[0]

    def clean_tmp_dir(self):
        if not os.path.isdir:
            os.mkdir(self.tmp_dir)
        else:
            shutil.rmtree(self.tmp_dir)

    def pc1_last25_pics(self):
        self.clean_tmp_dir()
        g_glob = glob.glob(self.tmp_dir_glob)

        new_pic_list = []
        if len(g_glob) == 0:
            return new_pic_list
        else:
            cur = con.cursor()
            cur.execute("""SELECT * FROM SecCams WHERE Camera='PiCam1' LIMIT 25;""")
            event_list = cur.fetchall()
            for event in event_list:
                tmp_file_name = ".".join((uuid.uuid4().hex, "jpg"))
                tmp_full_path = "/".join((self.tmp_dir, tmp_file_name))
                with Image.open(tmp_full_path, "w+") as pc1_file:
                    pc1_file.write(event.Picture)
                    new_pic_list.append(pc1_file)
            cur.close()
            return new_pic_list



class Pc2Sql:
    def pc2_log_last_moving(self):
        cur = con.cursor()
        cur.execute("""SELECT Tail FROM SecCamLogs WHERE Body='PiCam2' AND Tail='moving' ORDER BY FullDate ASC LIMIT 1;""")
        # cur.execute("SELECT Tail FROM SecCamLogs WHERE Tail='moving' LIMIT 24")
        z = cur.fetchone()
        cur.close()
        return z[0]

    def pc2_log_last_still(self):
        cur = con.cursor()
        cur.execute("""SELECT Tail FROM SecCamLogs WHERE Body='PiCam2' AND Tail='still' ORDER BY FullDate ASC LIMIT 1;""")
        x = cur.fetchone()
        cur.close()
        return x[0]







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
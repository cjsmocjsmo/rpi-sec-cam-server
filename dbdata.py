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
        return a

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
        return health_checks


#         self.upload = re.compile("Request to files/upload")

class Pc1Sql:
    def pc1_log_last_moving(self):
        cur = con.cursor()
        cur.execute("""SELECT Tail FROM SecCamLogs WHERE Body='PiCam1' AND Tail='moving' ORDER BY FullDate ASC LIMIT 1;""")
        z = cur.fetchone()
        cur.close()
        return z

    def pc1_log_last_still(self):
        cur = con.cursor()
        cur.execute("""SELECT Tail FROM SecCamLogs WHERE Body='PiCam1' AND Tail='still' ORDER BY FullDate ASC LIMIT 1;""")
        x = cur.fetchone()
        cur.close()
        return x

    def pc1_last25_pics(self):
        tmp_dir = "/tmp/SecCams"
        if not os.path.isdir:
            os.mkdir(tmp_dir)
        g_tmp_dir = "/tmp/SecCams/*.jpg"
        g_glob = glob.glob(g_tmp_dir)

        if len(g_glob) == 0:
            return None
        else:
            new_pic_list = []
            cur = con.cursor()
            cur.execute("""SELECT * FROM SecCams WHERE Camera='PiCam1' LIMIT 25;""")
            event_list = cur.fetchall()
            for event in event_list:
                tmp_file_name = ".".join((uuid.uuid4().hex, "jpg"))
                tmp_full_path = "/".join((tmp_dir, tmp_file_name))
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
        return z

    def pc2_log_last_still(self):
        cur = con.cursor()
        cur.execute("""SELECT Tail FROM SecCamLogs WHERE Body='PiCam2' AND Tail='still' ORDER BY FullDate ASC LIMIT 1;""")
        x = cur.fetchone()
        return x







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
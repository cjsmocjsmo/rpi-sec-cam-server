#!/usr/bin/python3
#    SecCam
#    Copyright (C) 2020  Charlie J Smotherman
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import re
import yaml
import json
import parselogs
import mydata
import glob
from pymongo import MongoClient
import subprocess
import tornado.web
import tornado.ioloop
import tornado.httpserver
from datetime import date
from urllib.parse import urlparse, parse_qs
from tornado.options import define, options, parse_command_line
from pprint import pprint 
import pymongo

from mydata import Conversions
SecCamClient = pymongo.MongoClient()
SecCamCon = SecCamClient.SecCam
PiCam1 = SecCamCon.picam1
PiCam2 = SecCamCon.picam2



PATH = '/media/pi/IMAGEHUB/imagehub_data'

# y = "/home/pi/imagehub_db_service/secCam.yaml"
# with open(y) as f:
#     conf = yaml.load(f)[0]

# print(conf["imagehub_port"])

cl = []
define('port', default=8090, help='run on the given port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        mpath = '/'.join((PATH, "images/"))
        # seccams = "/tmp/secCams/SEC/"
        handlers = [
            (r"/CamShots/(.*)", BaseJPGHandler, {'path': mpath}),
            (r"/main", MainHandler),
            (r"/db_file_size", db_file_sizeHandler),
            (r"/image_folder_size", image_folder_sizeHandler),
            (r"/total_size_on_disk", total_size_on_diskHandler),
            (r"/pingpc", ping_pcHandler),
            (r"/total_disk_size_in_db", total_disk_size_in_dbHandler),
            (r"/pc1_todays_events", pc1_todays_eventsHandler),
            (r"/pc2_todays_events", pc2_todays_eventsHandler),
            (r"/all_events", all_eventsHandler),
            (r"/pc1_last_fifty_pics", pc1_last_fifty_picsHandler),
            (r"/pc2_last_fifty_pics", pc2_last_fifty_picsHandler),
            (r"/all_pc1_pic_size", all_pc1_pic_sizeHandler),
            (r"/all_pc2_pic_size", all_pc2_pic_sizeHandler),
            (r"/all_pics_size", all_pics_sizeHandler),
            (r"/pc1_last_still", pc1_last_stillHandler),
            (r"/pc2_last_still", pc2_last_stillHandler),
            (r"/pc1_last_moving", pc1_last_movingHandler),
            (r"/pc2_last_moving", pc2_last_movingHandler),

            (r"/health", healthHandler),
            (r"/gd_gm_pep_status", gd_gm_pep_statusHandler),
            (r"/last_gd", last_gdHandler),
            (r"/last_gm", last_gmHandler),
            (r"/last_pep", last_pepHandler),





            
        ]
        settings = dict(
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            debug = True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)

class BaseJPGHandler(tornado.web.StaticFileHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Authorization")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "image/jpeg")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header("Access-Control-Allow-Headers", "access-control-allow-origin,authorization,content-type") 

class MainHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render('secCam.html')

class all_pc1_pic_sizeHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        pipe = [{'$group': {'_id': None, 'total': {'$sum': '$Size'}}}]
        pc1 = PiCam1.aggregate(pipeline=pipe)
        pc1_total_size_bytes = Conversions().convert_size(pc1['result'][0]['total'])
        self.write(dict(pc1_total_size_bytes=[pc1_total_size_bytes]))

class all_pc2_pic_sizeHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        pipe = [{'$group': {'_id': None, 'total': {'$sum': '$Size'}}}]
        pc2 = PiCam2.aggregate(pipeline=pipe)
        print(pc2['result'][0]['total'])
        pc2_total_size_bytes = Conversions().convert_size(pc2['result'][0]['total'])
        self.write(dict(pc2_total_size_bytes=[pc2_total_size_bytes]))

class all_pics_sizeHandler(BaseHandler):
    @tornado.gen.coroutine
    def pc1_total(self):
        pipe = [{'$group': {'_id': None, 'total': {'$sum': '$Size'}}}]
        pc1 = PiCam1.aggregate(pipeline=pipe)
        return pc1['result'][0]['total']

    @tornado.gen.coroutine
    def pc2_total(self):
        pipe = [{'$group': {'_id': None, 'total': {'$sum': '$Size'}}}]
        pc2 = PiCam2.aggregate(pipeline=pipe)
        return pc2['result'][0]['total']

    @tornado.gen.coroutine
    def get(self):
        pc1 = yield self.pc1_total()
        pc2 = yield self.pc2_total()
        total = pc1 + pc2
        size = Conversions().convert_size(total)
        self.write(dict(total_size=[size]))



class db_file_sizeHandler(BaseHandler):
    @tornado.gen.coroutine
    def db_stats(self):
        con = MongoClient()
        db_seccam = con['SecCam']
        db_scl = con['SCL']
        db_seccam_stats = db_seccam.command("dbStats")
        seccam_size_in_bytes = db_seccam_stats['fileSize']
        scl_stats = db_scl.command("dbstats")
        scl_size_in_bytes = scl_stats['fileSize']
        total_size = seccam_size_in_bytes + scl_size_in_bytes

        if total_size < 1048576:
            kb = total_size / 1024
            a1 = "{}KB".format(str(kb))
            print(a1)
            return a1
        elif total_size < 1073741824:
            mb = total_size / (1024*1024)
            b1 = "{}MB".format(str(mb))
            print(b1)
            return b1
        elif total_size > 1073741824:
            gb = total_size / (1024*1024*1024)
            c1 = "{}GB".format(str(gb))
            print(c1)
            return c1
        else:
            print("GUUUUUUUP")



        # total_size = total_size / (1024*1024)
        # size = str(total_size)
        # zize = "{}M".format(size[:5])
        # return zize

    @tornado.gen.coroutine
    def get(self):
        db_file_size = yield self.db_stats()
        self.write(dict(db_file_size=db_file_size))

class image_folder_sizeHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        path = '/'.join((PATH, 'images'))
        size = subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8')
        self.write(dict(image_folder_size=size))

class total_size_on_diskHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        size = subprocess.check_output(['du','-sh', PATH]).split()[0].decode('utf-8')
        self.write(dict(total_size_on_disk=size))

# class pic_dir_sizeHandler(BaseHandler):
#     @tornado.gen.coroutine
#     def get(self):
#         path = "/".join((PATH, "images"))
#         events = subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8') + "B"
#         self.write(dict(pic_dir_size=[events]))

class total_disk_size_in_dbHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        events = subprocess.check_output(['du','-sh', PATH]).split()[0].decode('utf-8') + "B"
        self.write(dict(total_disk=[events]))












class pc1_last_movingHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        command = "tail -n 3000 /media/pi/IMAGEHUB/imagehub_data/logs/imagehub.log | grep 'PiCam1|motion|moving'"
        result = os.popen(command, 'r', 1)
        result_list = []
        for r in result:
            result_list.append(r)
        lresult = len(result_list)
        if lresult < 1:
            self.write(dict(pc1_last_moving=["None", "None"]))
        elif lresult == 1:
            event = result_list[0].split(",")[0]
            datE, timE = event.split(" ")
            self.write(dict(pc1_last_moving=[datE, timE]))
        else:
            last_moving = result_list.pop()
            event = last_moving.split(",")[0]
            datE, timE = event.split(" ")
            self.write(dict(pc1_last_moving=[datE, timE]))
    

class pc2_last_movingHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        command = "tail -n 3000 /media/pi/IMAGEHUB/imagehub_data/logs/imagehub.log | grep 'PiCam2|motion|moving'"
        result = os.popen(command, 'r', 1)
        result_list = []
        for r in result:
            result_list.append(r)
        lresult = len(result_list)
        if lresult < 1:
            self.write(dict(pc2_last_moving=["None", "None"]))
        elif lresult == 1:
            event = result_list[0].split(",")[0]
            datE, timE = event.split(" ")
            self.write(dict(pc2_last_moving=[datE, timE]))
        else:
            last_moving = result_list.pop()
            event = last_moving.split(",")[0]
            datE, timE = event.split(" ")
            self.write(dict(pc2_last_moving=[datE, timE]))















class healthHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        command = "tail -n 30000 /media/pi/IMAGEHUB/imagehub_data/logs/imagehub.log | grep 'No messages received'"
        result = os.popen(command, 'r', 1)
        result_list = []
        for r in result:
            result_list.append(r)
        lresult = len(result_list)
        if lresult < 1:
            self.write(dict(last_health=["None"]))
        elif lresult == 1:
            last_health = result_list[0].split(",")[0]
            datE, timE = last_health.split(" ")
            self.write(dict(last_health=[datE, timE]))
        else:
            last_health = result_list.pop()
            lastHealth = last_health.split(",")[0]
            datE, timE = lastHealth.split(" ")
            self.write(dict(last_health=[datE, timE]))


class pc1_last_stillHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        command = "tail -n 3000 /media/pi/IMAGEHUB/imagehub_data/logs/imagehub.log | grep 'PiCam1|motion|still'"
        result = os.popen(command, 'r', 1)
        result_list = []
        for r in result:
            result_list.append(r)
        lresult = len(result_list)
        if lresult < 1:
            self.write(dict(pc1_last_still=["None", "None"]))
        elif lresult == 1:
            event = result_list[0].split(",")[0]
            datE, timE = event.split(" ")
            self.write(dict(pc1_last_still=[datE, timE]))
        else:
            last_still = result_list.pop()
            event = last_still.split(",")[0]
            datE, timE = event.split(" ")
            self.write(dict(pc1_last_still=[datE, timE]))

class pc2_last_stillHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        command = "tail -n 3000 /media/pi/IMAGEHUB/imagehub_data/logs/imagehub.log | grep 'PiCam2|motion|still'"
        result = os.popen(command, 'r', 1)
        result_list = []
        for r in result:
            result_list.append(r)
        lresult = len(result_list)
        if lresult < 1:
            self.write(dict(pc2_last_still=["None", "None"]))
        elif lresult == 1:
            event = result_list[0].split(",")[0]
            datE, timE = event.split(" ")
            self.write(dict(pc2_last_still=[datE, timE]))
        else:
            last_still = result_list.pop()
            event = last_still.split(",")[0]
            datE, timE = event.split(" ")
            self.write(dict(pc2_last_still=[datE, timE]))

class pc1_todays_eventsHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        events = mydata.DbData().piCam1_all_today_events()
        self.write(dict(pc1_todays_events=[events]))

class pc2_todays_eventsHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        events = mydata.DbData().piCam2_all_today_events()
        self.write(dict(pc2_todays_events=[events]))

class all_eventsHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        mydataa = mydata.DbData().all_events()
        self.write(dict(all_events=[mydataa]))

class ping_pcHandler(BaseHandler):
    @tornado.gen.coroutine
    def pc1_ping(self):
        pc1 = "192.168.0.61"
        cmd = "ping -c 2 {}".format(pc1)
        response = os.system(cmd)
        if response == 0:
            return 'Up!'
        else:
            return 'DOWN!'

    @tornado.gen.coroutine
    def pc2_ping(self):
        pc2 = "192.168.0.31"
        cmd = "ping -c 2 {}".format(pc2)
        response = os.system(cmd)
        if response == 0:
            return 'Up!'
        else:
            return 'DOWN!'

    @tornado.gen.coroutine
    def get(self):
        pc1 = yield self.pc1_ping()
        pc2 = yield self.pc2_ping()
        result = [pc1, pc2]
        self.write(dict(ping_results=result))

class gd_gm_pep_statusHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        status = mydata.DbData().gd_gm_pep_current_status()
        self.write(dict(status=status))

class pc1_last_fifty_picsHandler(BaseHandler):
    @tornado.gen.coroutine
    def get_today(self):
        d1 = date.today()
        return d1.strftime("%Y-%m-%d")

    @tornado.gen.coroutine
    def get_prefix(self):
        today = yield self.get_today()
        prefix = "http://192.168.0.26:8090/CamShots/" + today
        return prefix

    @tornado.gen.coroutine
    def glob_pic_dir(self):
        picdir = yield self.get_today()
        globdir = "/media/pi/IMAGEHUB/imagehub_data/images/" + picdir + "/*.jpg"
        picglob = glob.glob(globdir)
        lenpicglob = len(picglob)
        if lenpicglob != 0:
            pc1list = []
            pc1 = re.compile("PiCam1")
            [pc1list.append(p) for p in picglob if re.search(pc1, p)]
            pcg = [os.path.split(p)[1] for p in pc1list]
            pcg.sort(reverse=True)
            if len(pcg) > 26:
                return pcg[:26]
            else:
                return pcg
        else:
            return None
            
    @tornado.gen.coroutine
    def get(self):
        prefix = yield self.get_prefix()
        picglob = yield self.glob_pic_dir()
        plist = ["/".join((prefix, p)) for p in picglob]
        self.write(dict(plist=plist))

class pc2_last_fifty_picsHandler(BaseHandler):
    @tornado.gen.coroutine
    def get_today(self):
        d1 = date.today()
        return d1.strftime("%Y-%m-%d")

    @tornado.gen.coroutine
    def get_prefix(self):
        today = yield self.get_today()
        prefix = "http://192.168.0.26:8090/CamShots/" + today
        return prefix

    @tornado.gen.coroutine
    def glob_pic_dir(self):
        picdir = yield self.get_today()
        globdir = "/media/pi/IMAGEHUB/imagehub_data/images/" + picdir + "/*.jpg"
        picglob = glob.glob(globdir)
        lenpicglob = len(picglob)
        if lenpicglob != 0:
            pc1list = []
            pc1 = re.compile("PiCam2")
            [pc1list.append(p) for p in picglob if re.search(pc1, p)]
            pcg = [os.path.split(p)[1] for p in pc1list]
            pcg.sort(reverse=True)
            if len(pcg) > 26:
                return pcg[:26]
            else:
                return pcg
        else:
            return None
            
    @tornado.gen.coroutine
    def get(self):
        prefix = yield self.get_prefix()
        picglob = yield self.glob_pic_dir()
        plist = ["/".join((prefix, p)) for p in picglob]
        self.write(dict(plist=plist))

class last_gdHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        lastgd = mydata.DbData().last_gd()
        self.write(dict(lastgd=lastgd))

class last_gmHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        lastgm = mydata.DbData().last_gm()
        self.write(dict(lastgm=lastgm))

class last_pepHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        lastpep = mydata.DbData().last_pep()
        self.write(dict(lastpep=lastpep))

class picam1_todays_eventsHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        p = parselogs.ParseLogs()
        p.copy_log_file()
        p.parse_logs()
        z = {
            "picam1": p.picam1_todays_events(),
        }
        for a in z["picam1"]:
            print(a) 
        pprint(z)
        self.write(z)

class picam2_todays_eventsHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        p = parselogs.ParseLogs()
        p.copy_log_file()
        p.parse_logs()
        z = {
            "picam2": p.picam2_todays_events()
        }
        pprint(z)
        self.write(z)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

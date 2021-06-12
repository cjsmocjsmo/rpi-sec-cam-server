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
import data
import glob
from pymongo import MongoClient
import subprocess
import tornado.web
import tornado.ioloop
import tornado.httpserver
# import tornado.websocket
from datetime import date
from urllib.parse import urlparse, parse_qs
from tornado.options import define, options, parse_command_line
from pprint import pprint 

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
            (r"/db_folder_size", db_folder_sizeHandler),
            (r"/image_folder_size",image_folder_sizeHandler),
            (r"/total_size_on_disk", total_size_on_diskHandler),
            (r"/pingpc1", ping_pc1Handler),
            (r"/pingpc2", ping_pc2Handler),
            (r"/stats", statsHandler),
            (r"/picam1_todays_events", picam1_todays_eventsHandler),
            (r"/picam2_todays_events", picam2_todays_eventsHandler),
            (r"/pc1_last25_pics", pc1_last25_picsHandler),
            (r"/pc2_last25_pics", pc2_last25_picsHandler),
            (r"/gd_gm_pep_status", gd_gm_pep_statusHandler),
            (r"/pc1_last_fifty_pics", pc1_last_fifty_picsHandler),
            (r"/last_gd", last_gdHandler),
            (r"/last_gm", last_gmHandler),
            (r"/last_pep", last_pepHandler),

            # (r'/ws', SocketHandler),
            (r"/status_post", status_postHandler),
            # (r"/DBCount", totalPicDBHandler),
            # (r"/SecCams/(.*)", tornado.web.StaticFileHandler, {'path': seccams}),
            # (r"/TVShows/(.*)", tornado.web.StaticFileHandler, {'path': TVShows}),
            # (r"/Pictures/(.*)", tornado.web.StaticFileHandler, {'path': Pictures}),
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

class db_folder_sizeHandler(BaseHandler):

    @tornado.gen.coroutine
    def db_stats(self):
        con = MongoClient()
        db_seccam = con['SecCam']
        db_scl = con['SCL']
        db_seccam_stats = db_seccam.command("dbStats")
        seccam_size_in_bytes = db_seccam_stats['fileSize']
        scl_stats = db_scl.command("dbstats")
        scl_size_in_bytes = scl_stats['fileSize']
        total_size_in_bytes = seccam_size_in_bytes + scl_size_in_bytes

        if total_size_in_bytes < 1048576:
            kb = total_size_in_bytes / 1024
            a1 = "{}KB".format(str(kb))
            print(a1)
            return a1
        elif total_size_in_bytes < 1073741824:
            mb = total_size_in_bytes / (1024*1024)
            b1 = "{}MB".format(str(mb))
            print(b1)
            return b1
        elif total_size_in_bytes > 1073741824:
            gb = total_size_in_bytes / (1024*1024*1024)
            c1 = "{}GB".format(str(gb))
            print(c1)
            return c1
        else:
            print("GUUUUUUUP")



        # total_size = total_size_in_bytes / (1024*1024)
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

class statsHandler(BaseHandler):

    @tornado.gen.coroutine
    def pic_dir_size(self):
        path = "/".join((PATH, "images"))
        return subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8') + "B"

    @tornado.gen.coroutine
    def total_disk_size(self):
        return subprocess.check_output(['du','-sh', PATH]).split()[0].decode('utf-8') + "B"

    @tornado.gen.coroutine
    def piCam1_last_moving(self):
        return data.DbData().piCam1_last_moving_event()

    @tornado.gen.coroutine
    def piCam2_last_moving(self):
        return data.DbData().piCam2_last_moving_event()

    @tornado.gen.coroutine
    def last_health(self):
        return data.DbData().all_health_checks()

    @tornado.gen.coroutine
    def piCam1_last_still(self):
        return data.DbData().piCam1_last_still_event()

    @tornado.gen.coroutine
    def piCam2_last_still(self):
        return data.DbData().piCam2_last_still_event()

    @tornado.gen.coroutine
    def piCam1_all_today_events(self):
        return data.DbData().piCam1_all_today_events()

    @tornado.gen.coroutine
    def piCam2_all_today_events(self):
        return data.DbData().piCam2_all_today_events()

    @tornado.gen.coroutine
    def all_Events(self):
        return data.DbData().all_events()

    @tornado.gen.coroutine
    def get(self):
        picDirSize = yield self.pic_dir_size()
        totalDiskSize = yield self.total_disk_size()
        last_health_event = yield self.last_health()
        piCam1_last_moving_event = yield self.piCam1_last_moving()
        piCam2_last_moving_event = yield self.piCam2_last_moving()
        piCam1_last_still_event = yield self.piCam1_last_still()
        piCam2_last_still_event = yield self.piCam2_last_still()
        piCam1_all_today = yield self.piCam1_all_today_events()
        piCam2_all_today = yield self.piCam2_all_today_events()
        all_events = yield self.all_Events()

        z = {
            "picDirSize": picDirSize,
            "totalDiskSize": totalDiskSize,
            "health": last_health_event,
            "picam1LM": piCam1_last_moving_event,
            "picam2LM": piCam2_last_moving_event,
            "picam1LS": piCam1_last_still_event,
            "picam2LS": piCam2_last_still_event,
            "picam1AllToday": piCam1_all_today,
            "picam2AllToday": piCam2_all_today,
            "totalEvents": all_events,
        }
        self.write(z)

class ping_pc1Handler(BaseHandler):
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
    def get(self):
        pc1 = yield self.pc1_ping()
        result = {
            "pc1": pc1,
        }
        self.write(result)

class ping_pc2Handler(BaseHandler):
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
        pc2 = yield self.pc2_ping()
        result = {
            "pc2": pc2,
        }
        self.write(result)

class pc1_last25_picsHandler(BaseJPGHandler):
    @tornado.gen.coroutine
    def get(self):
        last25 = data.DbData().piCam1_last25_images()
        self.write(dict(last25=last25))

class pc2_last25_picsHandler(BaseJPGHandler):
    @tornado.gen.coroutine
    def get(self):
        last25 = data.DbData().piCam2_last25_images()
        self.write(dict(last25=last25))

class gd_gm_pep_statusHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        status = data.DbData().gd_gm_pep_current_status()
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

class last_gdHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        lastgd = data.DbData().last_gd()
        self.write(dict(lastgd=lastgd))

class last_gmHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        lastgm = data.DbData().last_gm()
        self.write(dict(lastgm=lastgm))

class last_pepHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        lastpep = data.DbData().last_pep()
        self.write(dict(lastpep=lastpep))

# class SocketHandler(tornado.websocket.WebSocketHandler):
#     def check_origin(self, origin):
#         return True

#     def open(self):
#         if self not in cl:
#             cl.append(self)

#     def on_close(self):
#         if self in cl:
#             cl.remove(self)

class status_postHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        gds = self.get_argument("GDStat")
        gms = self.get_argument("GMStat")
        peps = self.get_argument("PEPStat")
        data = gds, gms, peps
        print(gds)
        print(gms)
        print(peps)
        data = json.dumps(data)
        for c in cl:
            c.write_message(data)


class picam1_todays_eventsHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        p = parselogs.ParseLogs()
        p.copy_log_file()
        p.parse_logs()
        z = {
            "picam1": p.picam1_todays_events(),
        }
        [print(a) for a in z["picam1"]]
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

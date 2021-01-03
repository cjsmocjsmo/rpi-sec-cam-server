#!/usr/bin/python
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
import yaml
import sqlite3

import subprocess
from urllib.parse import urlparse, parse_qs
# from PIL import Image

# import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line

import dbfactory
import parselogs
import processpics

from pprint import pprint 

y = "/home/pi/imagehub_db_service/secCam.yaml"
with open(y) as f:
    conf = yaml.load(f)[0]

print(conf["imagehub_port"])

define('port', default=conf["imagehub_port"], help='run on the given port', type=int)

# processpics.ProcessSecCamPics().main()

class Application(tornado.web.Application):
    def __init__(self):
        mpath = "/media/pi/IMAGEHUB/imagehub_data/images/20-12-03"
        handlers = [
            (r"/CamShots/(.*)", tornado.web.StaticFileHandler, {'path': mpath}),
            (r"/Main", MainHandler),
            (r"/Picam1_todays_events", picam1_todays_eventsHandler),
            (r"/Picam2_todays_events", picam2_todays_eventsHandler),

            (r"/Picam1_last_moving_event", picam1_last_moving_eventHandler),
            (r"/Picam2_last_moving_event", picam2_last_moving_eventHandler),

            (r"/Picam1_last_still_event", picam1_last_still_eventHandler),
            (r"/Picam2_last_still_event", picam2_last_still_eventHandler),

            
            # (r"piCam1_last_ten_moving_event", piCam1_last_ten_moving_eventHandler),
            # (r"piCam2_last_ten_moving_event", piCam2_last_ten_moving_eventHandler),
 
            (r"/Last_health_event", last_health_eventHandler),
            (r"/PingPiCam1", ping_picams1Handler),
            (r"/PingPiCam2", ping_picams2Handler),

            (r"/DBsize", dbsizeHandler),
            # (r"/Movies/(.*)", tornado.web.StaticFileHandler, {'path': Movies}),
            # (r"/TVShows/(.*)", tornado.web.StaticFileHandler, {'path': TVShows}),
            # (r"/Pictures/(.*)", tornado.web.StaticFileHandler, {'path': Pictures}),
        ]
        settings = dict(
            # port = conf["imagehub_port"],
            static_path = "/home/pi/rpi-sec-cam-server/static",
            # static_path = os.path.join(os.path.dirname(__file__), "static"),
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            debug = True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")
        # self.set_header("Cache-Control", "max-age=370739520, public")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)

class MainHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render('secCam.html')

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

class picam1_last_moving_eventHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        p = parselogs.ParseLogs()
        p.copy_log_file()
        p.parse_logs()
        z = {
            "picam1": p.piCam1_last_moving_event()
        }
        print(z)
        self.write(z)

class picam2_last_moving_eventHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        p = parselogs.ParseLogs()
        p.copy_log_file()
        p.parse_logs()
        z = {
            "picam2": p.piCam2_last_moving_event()
        }
        print(z)
        self.write(z)

class picam1_last_still_eventHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        p = parselogs.ParseLogs()
        p.copy_log_file()
        p.parse_logs()
        z = {
            "picam1": p.piCam1_last_still_event()
        }
        print(z)
        self.write(z)

class picam2_last_still_eventHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        p = parselogs.ParseLogs()
        p.copy_log_file()
        p.parse_logs()
        z = {
            "picam2": p.piCam2_last_still_event()
        }
        print(z)
        self.write(z)

class dbsizeHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")
        self.set_header("Cache-Control", "max-age=370739520, public")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)

    @tornado.gen.coroutine
    def get(self):
        dbf = dbfactory.DbFactory()
        size = dbf.dbsize()
        self.write(dict(dbs=size))

class last_health_eventHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        p = parselogs.ParseLogs()
        p.copy_log_file()
        p.parse_logs()
        lhe = p.last_health_event()
        result = ""
        if lhe != None:
            result = lhe
        else:
            result = ["None noted"]

        z = {
            "lasthealthevent": result
        }
        print(z)
        self.write(z)

class ping_picams1Handler(BaseHandler):
    @tornado.gen.coroutine
    def pc1_ping(self):
        pc1 = "192.168.0.61"
        cmd = "ping -c 5 {}".format(pc1)
        response = os.system(cmd)
        if response == 0:
            return 'PiCam1 is up!'
        else:
            return 'PiCam1 is down!'

    @tornado.gen.coroutine
    def get(self):
        pc1 = yield self.pc1_ping()
        result = {
            "pc1": pc1,
        }
        self.write(result)

class ping_picams2Handler(BaseHandler):
    @tornado.gen.coroutine
    def pc2_ping(self):
        pc2 = "192.168.0.31"
        cmd = "ping -c 5 {}".format(pc2)
        response = os.system(cmd)
        if response == 0:
            return 'PiCam2 is up!'
        else:
            return 'PiCam2 is down!'

    @tornado.gen.coroutine
    def get(self):
        pc2 = yield self.pc2_ping()
        result = {
            "pc2": pc2,
        }
        self.write(result)





# class last_(tornado.web.RequestHandler):


# class WeeklyEventsHandler(tornado.web.RequestHandler):
#     @tornado.gen.coroutine
#     def get(self):
#         print("o")
        # l = [sh for sh in db.movietime2DB.find({"Catagory":"Men In Black"}, {"_id":0})]
        # self.write(dict(IntMenInBlack=l))

# class MonthlyEventsHandler(tornado.web.RequestHandler):
#     @tornado.gen.coroutine
#     def get(self):
#         print("o")

# class TotalEventsHandler(tornado.web.RequestHandler):
#     @tornado.gen.coroutine
#     def get(self):
#         print("o")

# class ClearEventsHandler(tornado.web.RequestHandler):
#     @tornado.gen.coroutine
#     def get(self):
#         print("o")





def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

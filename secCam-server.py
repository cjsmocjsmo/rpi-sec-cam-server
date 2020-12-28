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

import parselogs
import processpics

from pprint import pprint 

with open('secCam.yaml') as f:
    conf = yaml.load(f)[0]

print(conf["imagehub_port"])

define('port', default=conf["imagehub_port"], help='run on the given port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        
        handlers = [
            (r"/Main", MainHandler),
            (r"/Picam1_todays_events", picam1_todays_eventsHandler),
            (r"/Picam2_todays_events", picam2_todays_eventsHandler),

            (r"/Picam1_last_moving_event", picam1_last_moving_eventHandler),
            (r"/Picam2_last_moving_event", picam2_last_moving_eventHandler),

            # (r"picam1_last_still_event", picam1_last_still_eventHandler),
            # (r"picam2_last_still_event", picam2_last_still_eventHandler),

            # (r"piCam1_last_ten_moving_event", piCam1_last_ten_moving_eventHandler),
            # (r"piCam2_last_ten_moving_event", piCam2_last_ten_moving_eventHandler),
 
            # (r"/last_health_event", last_health_eventHandler),

            # (r"/Movies/(.*)", tornado.web.StaticFileHandler, {'path': Movies}),
            # (r"/TVShows/(.*)", tornado.web.StaticFileHandler, {'path': TVShows}),
            # (r"/Pictures/(.*)", tornado.web.StaticFileHandler, {'path': Pictures}),
        ]
        settings = dict(
            # port = conf["imagehub_port"],
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            debug = True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render('secCam.html')

class picam1_todays_eventsHandler(tornado.web.RequestHandler):
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

class picam2_todays_eventsHandler(tornado.web.RequestHandler):
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

class picam1_last_moving_eventHandler(tornado.web.RequestHandler):
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

class picam2_last_moving_eventHandler(tornado.web.RequestHandler):
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

# class StopHandler(tornado.web.RequestHandler):
#     @tornado.gen.coroutine
#     def get(self):
#         stop_cmd = ["bash", os.environ["MT_DBUSCONTROLPATH"], "stop"]
#         subprocess.call(stop_cmd)

# class NextHandler(tornado.web.RequestHandler):
#     @tornado.gen.coroutine
#     def get(self):
#         next_seek_cmd = ["bash", os.environ["MT_DBUSCONTROLPATH"], "seek", "60000000"]
#         subprocess.call(next_seek_cmd)

# class PreviousHandler(tornado.web.RequestHandler):
#     @tornado.gen.coroutine
#     def get(self):
#         previous_seek_cmd = ["bash", os.environ["MT_DBUSCONTROLPATH"], "seek", "-30000000"]
#         subprocess.call(previous_seek_cmd)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    processpics.ProcessSecCamPics().main()

if __name__ == "__main__":
    main()

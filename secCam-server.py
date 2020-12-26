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

with open('secCam.yaml') as f:
    conf = yaml.load(f, Loader=yaml.FullLoader)[0]
define('port', default=conf["imagehub_port"], help='run on the given port', type=int)

class Application(tornado.web.Application):
    def __init__(self):

        handlers = [
            (r"picam1_todays_events", picam1_todays_eventsHandler),
            (r"picam2_todays_events", picam2_todays_eventsHandler),

            (r"picam1_last_moving_event", picam1_last_moving_eventHandler),
            (r"picam2_last_moving_event", picam2_last_moving_eventHandler),

            (r"picam1_last_still_event", picam1_last_still_eventHandler),
            (r"picam2_last_still_event", picam2_last_still_eventHandler),

            (r"piCam1_last_ten_moving_event", piCam1_last_ten_moving_eventHandler),
            (r"piCam2_last_ten_moving_event", piCam2_last_ten_moving_eventHandler),
 
            (r"/last_health_event", last_health_eventHandler),

            # (r"/Movies/(.*)", tornado.web.StaticFileHandler, {'path': Movies}),
            # (r"/TVShows/(.*)", tornado.web.StaticFileHandler, {'path': TVShows}),
            # (r"/Pictures/(.*)", tornado.web.StaticFileHandler, {'path': Pictures}),
        ]
        settings = dict(
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            debug = True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

# class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.render('secCam.html')

class picam1_todays_eventsHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        pl = parselogs.Parselogs().copy_log_file().parse_logs()
        z = {
            "picam1": pl.picam1_todays_events(),
            "picam2": pl.picam2_todays_events()
        }
        self.write(z)

class WeeklyEventsHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        print("o")
        # l = [sh for sh in db.movietime2DB.find({"Catagory":"Men In Black"}, {"_id":0})]
        # self.write(dict(IntMenInBlack=l))

# class MonthlyEventsHandler(tornado.web.RequestHandler):
#     @tornado.gen.coroutine
#     def get(self):
#         print("o")

class TotalEventsHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        print("o")


class ClearEventsHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        print("o")







class StopHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        stop_cmd = ["bash", os.environ["MT_DBUSCONTROLPATH"], "stop"]
        subprocess.call(stop_cmd)

class NextHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        next_seek_cmd = ["bash", os.environ["MT_DBUSCONTROLPATH"], "seek", "60000000"]
        subprocess.call(next_seek_cmd)

class PreviousHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        previous_seek_cmd = ["bash", os.environ["MT_DBUSCONTROLPATH"], "seek", "-30000000"]
        subprocess.call(previous_seek_cmd)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

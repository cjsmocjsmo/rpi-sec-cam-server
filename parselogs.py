#/usr/bin/python3
#    MovieGo
#    Copyright (C) 2017  Charlie J Smotherman
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
import time
import string
import shutil
from pprint import pprint
import yaml
from datetime import date
import filecmp

class ParseLogs:
    def __init__(self):
        with open('secCam.yaml') as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)[0]
        d1 = date.today()
        self.today = d1.strftime("%Y-%m-%d")
        self.log_file = self.conf["log_file_path"]
        self.log_file_copy = self.conf["log_file_copy_path"]
        self.pc1 = re.compile("PiCam1")
        self.pc2 = re.compile("PiCam2")
        self.moving = re.compile("moving")
        self.still = re.compile("still")
        self.health = re.compile("No messages received for 60 minutes")
        self.pc1_moving_events = []
        self.pc1_still_events = []
        self.pc2_moving_events = []
        self.pc2_still_events = []
        self.healthEvents = []
        self.allEvents = []

    def copy_log_file(self):
        if os.path.isfile(self.log_file_copy):
            comp = filecmp.cmp(self.log_file, self.log_file_copy, shallow = False)
            if comp:
                shutil.copyfile(self.log_file, self.log_file_copy)
        else:
            shutil.copyfile(self.log_file, self.log_file_copy)


    def parse_logs(self):
        with open(self.log_file_copy) as in_file:
            for line in in_file:
                self.allEvents.append(line)
                if (self.pc1.search(line)):
                    if (self.moving.search(line)):
                        far = line.replace("\n", "")
                        self.pc1_moving_events.append(far)
                    elif (self.still.search(line)):
                        bar = line.replace("\n", "")
                        self.pc1_still_events.append(bar)
                    else:
                        print("boo")
                elif (self.pc2.search(line)):
                    if (self.moving.search(line)):
                        out = line.replace("\n", "")
                        self.pc2_moving_events.append(out)
                    elif (self.still.search(line)):
                        bar = line.replace("\n", "")
                        self.pc2_still_events.append(bar)
                    else:
                        print("moo")
                elif (self.health.search(line)):
                    dude = line.replace("\n", "")
                    self.healthEvents.append(dude)
                else:
                    pass

    def split_string(self, astr):
        date2, stat = astr.split(" ~ ")
        date1 = date2[:-4]
        datE, timE = date1.split(" ", 1)
        if not self.health.search(astr):
            stat2 = stat.split("|", 2)
            camera = stat2[0]
            status = stat2[2]
            return (camera, status, datE, timE)
        else:
            return (datE, timE, stat)

    def picam1_todays_events(self):
        todays_events = []
        for ev in self.allEvents:
            if (self.pc1.search(ev)) and (self.today.search(ev)):
                todays_events.append(ev)
        return todays_events

    def picam2_todays_events(self):
        todays_events = []
        for ev in self.allEvents:
            if (self.pc2.search(ev)) and (self.today.search(ev)):
                todays_events.append(ev)
        return todays_events

    def piCam1_all_events(self):
        pc1ae = []
        [pc1ae.append(ev) for ev in self.allEvents if (self.pc1.search(ev))]
        # for ev in self.allEvents:
        #     if (self.pc1.search(ev)):
        #         pc1ae.append(ev)
        return pc1ae

    def piCam2_all_events(self):
        pc2ae = []
        [pc2ae.append(ev) for ev in self.allEvents if (self.pc2.search(ev))]
        # for ev in self.allEvents:
        #     if (self.pc2.search(ev)):
        #         pc2ae.append(ev)
        return pc2ae

    def piCam1_last_moving_event(self):
        elen = len(self.pc1_moving_events)
        if elen > 1:
            last = elen - 1
            return [self.split_string(a) for a in self.pc1_moving_events[last:]][0]
        elif elen == 1:
            return [self.split_string(a) for a in self.pc1_moving_events][0]
        else:
            return None

    def piCam1_last_ten_moving_event(self):
        elen = len(self.pc1_moving_events)
        if elen > 9:
            last = elen - 10
            foo = [self.split_string(a) for a in self.pc1_moving_events[last:]]
            return foo
        elif elen < 10:
            return [self.split_string(a) for a in self.pc1_moving_events]
        else:
            return None

    def piCam1_last_still_event(self):
        elen = len(self.pc1_still_events)
        if elen > 1:
            last = elen - 1
            return [self.split_string(a) for a in self.pc1_still_events[last:]][0]
        elif elen == 1:
            return [self.split_string(a) for a in self.pc1_still_events][0]
        else:
            return None

    def piCam2_last_moving_event(self):
        elen = len(self.pc2_moving_events)
        if elen > 1:
            last = elen - 1
            return [self.split_string(a) for a in self.pc2_moving_events[last:]][0]
        elif elen == 1:
            return [self.split_string(a) for a in self.pc2_moving_events][0]
        else:
            return None

    def piCam2_last_ten_moving_event(self):
        elen = len(self.pc2_moving_events)
        if elen > 9:
            last = elen - 10
            return [self.split_string(a) for a in self.pc2_moving_events[last:]]
        elif elen < 10:
            return [self.split_string(a) for a in self.pc2_moving_events]
        else:
            return None

    def piCam2_last_still_event(self):
        elen = len(self.pc2_still_events)
        if elen > 1:
            last = elen - 1
            return [self.split_string(a) for a in self.pc2_still_events[last:]][0]
        elif elen == 1:
            return [self.split_string(a) for a in self.pc2_still_events][0]
        else:
            return None

    def last_health_event(self):
        elen = len(self.healthEvents)
        if elen > 1:
            last = elen - 1
            return [self.split_string(a) for a in self.healthEvents[last:]]
        elif elen == 1:
            return self.split_string(self.healthEvents[0])
        else:
            return None


    def main(self):
        self.copy_log_file()
        self.parse_logs()
        x = {
            "picam1_todays_events": picam1_todays_events(),
            "picam2_todays_events": picam2_todays_events(),
            "picam1_last_moving_event": self.piCam1_last_moving_event(),
            "picam2_last_moving_event": self.piCam2_last_moving_event(),
            "picam1_last_still_event": self.piCam1_last_still_event(),
            "picam2_last_still_event": self.piCam2_last_still_event(),
            "piCam1_last_ten_moving_event": self.piCam1_last_ten_moving_event(),
            "piCam2_last_ten_moving_event": self.piCam2_last_ten_moving_event(),
            "last_health_event": self.last_health_event(),
        }
        pprint(x)
        # os.remove(self.log_file_copy)


if __name__ == "__main__":
    pl = ParseLogs()
    pl.main()

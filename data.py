#!/usr/bin/python3

# import os
from datetime import date
# from pathlib import Path
from pymongo import MongoClient
from pprint import pprint

con = MongoClient()

db = con['SecCam']
PiCam1 = db['picam1']
PiCam2 = db['picam2']

con = MongoClient()
db2 = con['SCL']
PiCamLogs = db2['pclogs']

class DbData:
    def __init__(self):
        d1 = date.today()
        self.today = d1.strftime("%Y-%m-%d")
        self.y, self.m, self.d = self.today.split("-", 2)

    def piCam1_last_moving_event(self):
        b1 = {"Body":"PiCam1", "Tail":"moving"}
        b2 = {"_id":0, "DateTimeMessage":0, "Message":0, "Year":0, "Month":0, "Day":0, "Hour":0, "Minute":0, "Second":0, "Millisecond":0}
        results = PiCamLogs.find(b1, b2).sort("DateTime", -1)
        return results[0]

    def piCam2_last_moving_event(self):
        b1 = {"Body":"PiCam2", "Tail":"moving"}
        b2 = {"_id":0, "DateTimeMessage":0, "Message":0, "Year":0, "Month":0, "Day":0, "Hour":0, "Minute":0, "Second":0, "Millisecond":0}
        results = PiCamLogs.find(b1, b2).sort("DateTime", -1)
        return results[0]

    def piCam1_last_still_event(self):
        b1 = {"Body":"PiCam1", "Tail":"still"}
        b2 = {"_id":0, "DateTimeMessage":0, "Message":0, "Year":0, "Month":0, "Day":0, "Hour":0, "Minute":0, "Second":0, "Millisecond":0}
        results = PiCamLogs.find(b1, b2).sort("DateTime", -1)
        return results[0]

    def piCam2_last_still_event(self):
        b1 = {"Body":"PiCam2", "Tail":"still"}
        b2 = {"_id":0, "DateTimeMessage":0, "Message":0, "Year":0, "Month":0, "Day":0, "Hour":0, "Minute":0, "Second":0, "Millisecond":0}
        results = PiCamLogs.find(b1, b2).sort("DateTime", -1)
        return results[0]
 
    def piCam1_all_today_events(self):
        b1 = {"Year":self.y, "Month":self.m, "Day":self.d, "Body":"PiCam1"}
        b2 = {"_id":0}
        search = PiCamLogs.find(b1, b2)
        results = [s for s in search]
        return len(results)
        
    def piCam2_all_today_events(self):
        b1 = {"Year":self.y, "Month":self.m, "Day":self.d, "Body":"PiCam2"}
        b2 = {"_id":0}
        search = PiCamLogs.find(b1, b2)
        results = [s for s in search]
        return len(results)

    def all_health_checks(self):
        b1 = {"Year":self.y, "Month":self.m, "Day":self.d, "Message":"No messages received for 60 minutes"}
        b2 = {"_id":0}
        search = PiCamLogs.find(b1,b2)
        results = [s for s in search]
        return len(results)

    def all_events(self):
        results = PiCamLogs.count()
        return results

    def piCam1_last25_images(self):
        b1 = {"Camera":"PiCam1", "Date":self.today}
        b2 = {"_id":0}
        results = PiCam1.find(b1,b2).sort("Date", -1).limit(25)
        http_path_list = []
        for r in results:
            _, file_path = r['Filename'].split('images/', 1)
            http = "http://192.168.0.26:8090/CamShots"
            http_path = "/".join((http, file_path))
            http_path_list.append(http_path)
        http_path_list.sort(reverse=True)
        return http_path_list

    def piCam2_last25_images(self):
        b1 = {"Camera":"PiCam2", "Date":self.today}
        b2 = {"_id":0}
        results = PiCam2.find(b1,b2).sort("Date", -1).limit(25)
        http_path_list = []
        for r in results:
            _, file_path = r['Filename'].split('images/', 1)
            http = "http://192.168.0.26:8090/CamShots"
            http_path = "/".join((http, file_path))
            http_path_list.append(http_path)
        http_path_list.sort(reverse=True)
        return http_path_list

    def gd_gm_pep_status(self):
        b1 = {"Camera":"PiCam2", "Date":self.today}
        b2 = {"_id":0}
        results = PiCam2.find(b1,b2).sort("Time", -1).limit(10)
        gdstat = ''
        gdprob = ''
        gmstat = ''
        gmprob = ''
        pepstat = ''
        pepprob = ''
        # results.sort("Time", -1)
        for r in results:
            pprint(r)
            gdstat = r["GDStat"]
            gdprob = r['GDProb']
            gmstat = r['GMStat']
            gmprob = r['GMProb']
            pepstat = r['PEPStat']
            pepprob = r['PEPProb']
        return gdstat, gdprob, gmstat, gmprob, pepstat, pepprob




if __name__ == '__main__' :
    db = DbData()
    print(db.gd_gm_pep_status())
    # print(db.piCam2_last25_images())
#     print(db.all_events())
#     print(db.all_health_checks())
#     print(db.piCam2_all_today_events())
#     print(db.piCam1_all_today_events())

#     # print(db.piCam2_last_still_event())
#     # print(db.piCam1_last_still_event())
    
#     # print(db.piCam2_last_moving_event())
#     print(db.piCam1_last_moving_event())
    
   
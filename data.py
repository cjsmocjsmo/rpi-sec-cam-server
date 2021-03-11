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
        b1 = {"Year":self.y, "Month":self.m, "Day":self.d, "Body":"PiCam1", "Tail":"moving"}
        b2 = {"_id":0}
        results = PiCamLogs.find_one(b1, b2)
        return results

    def piCam2_last_moving_event(self):
        b1 = {"Year":self.y, "Month":self.m, "Day":self.d, "Body":"PiCam2", "Tail":"moving"}
        b2 = {"_id":0}
        results = PiCamLogs.find_one(b1, b2)
        return results

    def piCam1_last_still_event(self):
        b1 = {"Year":self.y, "Month":self.m, "Day":self.d, "Body":"PiCam1", "Tail":"moving"}
        b2 = {"_id":0}
        results = PiCamLogs.find_one(b1, b2)
        return results

    def piCam2_last_still_event(self):
        b1 = {"Year":self.y, "Month":self.m, "Day":self.d, "Body":"PiCam2", "Tail":"moving"}
        b2 = {"_id":0}
        results = PiCamLogs.find_one(b1, b2)
        return results
 
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

if __name__ == '__main__' :
    db = DbData()
    print(db.all_events())
    print(db.all_health_checks())
    print(db.piCam2_all_today_events())
    print(db.piCam1_all_today_events())

    # print(db.piCam2_last_still_event())
    # print(db.piCam1_last_still_event())
    
    # print(db.piCam2_last_moving_event())
    print(db.piCam1_last_moving_event())
    
   
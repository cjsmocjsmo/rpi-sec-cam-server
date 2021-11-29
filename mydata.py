#!/usr/bin/python3

# import os
from datetime import date
# from pathlib import Path
import pymongo
from pprint import pprint



SecCamClient = pymongo.MongoClient()
SecCamCon = SecCamClient.SecCam
PiCam1 = SecCamCon.picam1
PiCam2 = SecCamCon.picam2

SCLClient = pymongo.MongoClient()
SCLCon = SCLClient.SCL
PiCamLogs = SCLCon.pclogs

print(PiCamLogs.count())

class DbData:
    def __init__(self):
        self.d1 = date.today()
        self.today = self.d1.strftime("%Y-%m-%d")
        self.y, self.m, self.d = self.today.split("-", 2)
 
    def piCam1_all_today_events(self):
        b1 = {"Year":self.y, "Month":self.m, "Day":self.d, "Camera":"PiCam1"}
        b2 = {"_id":0}
        search = PiCamLogs.find(b1, b2)
        results = [s for s in search]
        #con.close()
        return len(results)
        
    def piCam2_all_today_events(self):
        b1 = {"Year":self.y, "Month":self.m, "Day":self.d, "Camera":"PiCam2"}
        b2 = {"_id":0}
        search = PiCamLogs.find(b1, b2)
        results = [s for s in search]
        #con.close()
        return len(results)

    def all_events(self):
        results = PiCamLogs.count()
        print(results)
        #con.close()
        return results







    def gd_gm_pep_current_status(self):
        b1 = {"Camera":"PiCam2", "Date":self.today}
        b2 = {"_id":0}
        results = PiCam2.find(b1,b2).sort("Time", -1).limit(1)
        #con.close()
        for r in results:
            return r["GDStat"], r['GDProb'], r['GMStat'], r['GMProb'], r['PEPStat'], r['PEPProb']

    def last_gd(self):
        b1 = {"Camera":"PiCam2", "GDStat":"open"}
        b2 = {"Camera":"PiCam2", "GDStat":"closed"}
        b3 = {"_id":0, "DateTimeMessage":0, "Message":0, "Year":0, "Month":0, "Day":0, "Hour":0, "Minute":0, "Second":0, "Millisecond":0}
        
        try:
            open_results = PiCam2.find(b1,b3).sort("Name", -1).limit(10)
            last_open_results = open_results[0]['GDStat'], open_results[0]['Date'], open_results[0]['Time'][:-7]
        except IndexError:
            last_open_results = "None", "None", "None", "None"

        try:
            closed_results = PiCam2.find(b2,b3).sort("Name", -1).limit(10)
            # for c in closed_results:
            #     pprint(c)
            last_closed_results = closed_results[0]['GDStat'], closed_results[0]['Date'], closed_results[0]['Time'][:-7]
        except IndexError:
            last_closed_results = "None", "None", "None", "None"
        #con.close()
        return last_open_results, last_closed_results
        
    def last_gm(self):
        b1 = {"Camera":"PiCam2", "GMStat":"home"}
        b2 = {"Camera":"PiCam2", "GMStat":"nothome"}
        b3 = {"_id":0, "DateTimeMessage":0, "Message":0, "Year":0, "Month":0, "Day":0, "Hour":0, "Minute":0, "Second":0, "Millisecond":0}
        
        try:
            home_results = PiCam2.find(b1,b3).sort("Name", -1).limit(1)
            last_home_results = home_results[0]['GMStat'], home_results[0]['Date'], home_results[0]['Time'][:-7]
        except IndexError:
            last_home_results = "None", "None", "None", "None"
        
        try:
            nothome_results = PiCam2.find(b2,b3).sort("Name", -1).limit(1)
            last_nothome_results = nothome_results[0]['GMStat'], nothome_results[0]['Date'], nothome_results[0]['Time'][:-7]
        except IndexError:
            last_nothome_results = "None", "None", "None", "None"
        #con.close()
        return last_home_results, last_nothome_results

    def last_pep(self):
        b1 = {"Camera":"PiCam2", "PEPStat":"people"}
        b2 = {"Camera":"PiCam2", "PEPStat":"notpeople"}
        b3 = {"_id":0, "DateTimeMessage":0, "Message":0, "Year":0, "Month":0, "Day":0, "Hour":0, "Minute":0, "Second":0, "Millisecond":0}
        
        try:
            pep_results = PiCam2.find(b1,b3).sort("Name", -1).limit(1)
            last_pep_results = pep_results[0]['PEPStat'], pep_results[0]['Date'], pep_results[0]['Time'][:-7]
        except IndexError:
            last_pep_results = "None", "None", "None", "None"

        try:
            notpep_results = PiCam2.find(b2,b3).sort("Name", -1).limit(1)
            last_notpep_results = notpep_results[0]['PEPStat'], notpep_results[0]['Date'], notpep_results[0]['Time'][:-7]
        except IndexError:
            last_notpep_results = "None", "None", "None", "None"
        #con.close()
        return last_pep_results, last_notpep_results


class Conversions:
    def convert_size(self, total_size):
        if total_size < 1048576:
            a1 = total_size / 1024
            a2 = str(a1)
            kb = a2[:6]
            return "{}KB".format(kb)
        elif total_size < 1073741824:
            b1 = total_size / (1024*1024)
            b2 = str(b1)
            mb = b2[:6]
            return "{}MB".format(mb)
        elif total_size > 1073741824:
            g1 = total_size / (1024*1024*1024)
            g2 = str(g1)
            gb = g2[:6]
            return "{}GB".format(gb)
        else:
            return total_size


if __name__ == '__main__' :
    db = DbData()
    print(db.last_gd())

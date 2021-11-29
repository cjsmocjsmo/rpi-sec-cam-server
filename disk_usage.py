#!/usr/bin/python3

# to generate a disk usage report used with cron


import os
import glob
import logging
import datetime

data_path = "/media/pi/IMAGEHUB/imagehub_data/images/"
report_path = "/media/pi/IMAGEHUB/ImageHubReports"
image_path = "/media/pi/IMAGEHUB/imagehub_data/images/*"
db_path = "/media/pi/IMAGEHUB/imagehub_data/db/*"
logs_path = "/media/pi/IMAGEHUB/imagehub_data/logs/*"

size_list = []
class DiskUsage:
    def __init__(self):
        self.pictotal = []
        self.count = 0
        logging.basicConfig(
            filename ='/home/pi/rpi-sec-cam-server/file_size_update.log',
            level = logging.DEBUG,
            format = '%(levelname)s:%(asctime)s:%(message)s',
        )

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

    def process_glob_db(self, apath):
        dbfiles = glob.glob(apath)
        db_list = []
        for db in dbfiles:
            fsize = os.stat(db).st_size
            db_list.append(fsize)
        # db_sum = self.convert_size(sum(db_list))
        dbpath = report_path + "/db_report.txt"
        with open(dbpath, "w") as report:
            report.write(str(sum(db_list)))

    def process_glob_log(self, apath):
        logfiles = glob.glob(apath)
        log_list = []
        for log in logfiles:
            fsize = os.stat(log).st_size
            log_list.append(fsize)
        # log_sum = self.convert_size(sum(log_list))
        rpath = report_path + "/log_report.txt"
        with open(rpath, "w") as report:
            report.write(str(sum(log_list)))

    def glob_main_image_dir(self, adir):
        dirlist = glob.glob(adir)
        dlist = sorted(dirlist)
        return dlist[:len(dlist) - 1]

    def todaysDate(self):
        today = datetime.datetime.now()
        return today.strftime("%Y-%m-%d")

    def glob_image_dir(self, adir):
        glob_pat = adir + "/*"
        picz = glob.glob(glob_pat)
        if "images_report.txt" in picz:
            print("images_report.txt exists already")
            pass
        else:
            piclist = []
            for pic in picz:
                print("Processing:\n {}".format(pic))
                fsize = os.stat(pic).st_size
                piclist.append(fsize)
            pic_sum = sum(piclist)
            self.pictotal.append(pic_sum)
            # new_pic_sum = self.convert_size(sum(self.pictotal))
            rpath = adir + "/images_report.txt"
            self.count += 1
            rrpath = report_path + "/images/" + str(self.count) + "images_report.txt"
            with open(rpath, "w") as report:
                report.write(str(pic_sum))
            with open(rrpath, "w") as report:
                report.write(str(pic_sum))

    def cleanup(self):
        for (paths, dirs, files) in os.walk(data_path):
            for filename in files:
                print("Processing:\n %s" % filename)
                fnn = os.path.join(paths, filename)
                if filename == "images_report.txt":
                    os.remove(fnn)

    def main(self):
        self.count = 0
        self.process_glob_db(db_path)
        self.process_glob_log(logs_path)
        img_dirs = self.glob_main_image_dir(image_path)
        for img in img_dirs:
            self.glob_image_dir(img)
        total = sum(self.pictotal)
        print(total)
    
    def check_for_update(self):
        count1 = 0
        for (paths, dirs, files) in os.walk(data_path):
            for filename in files:
                if filename == "images_report.txt":
                    count1 += 1
        glp = report_path + "/images/*"
        count2 = len(glob.glob(glp))
        print(count1)
        print(count2)
        logging.debug(count1)
        logging.debug(count2)
        if count1 != count2:
            logging.debug("Starting main")
            self.main()
        else:
            print("No update needed")
            logging.debug("No update needed")

if __name__ == "__main__":
    DU = DiskUsage()
    DU.check_for_update()

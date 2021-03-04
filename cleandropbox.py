#!/usr/bin/python3

import os
import glob

dbox_dir = "/home/teresa/Dropbox/Apps/ppcam/ppcam/*.jpg"
dbox_files = glob.glob(dbox_dir)
lbf = len(dbox_files)
if lbf > 0:
    for f in dbox_files:
        os.remove(f)


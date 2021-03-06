#!/usr/bin/python3

from pathlib import Path


def read_file(afile):
    value = ""
    with open(afile, "r+") as rf:
        value = rf.read()
    return value

def write_file(afile, avalue):
    with open(afile, "w+") as wf:
        wf.write(str(avalue))

def image_data(image):
    with open(image, "br") as img:
        return img.read()

def create_pc1_new_files(pc1gdcount_path):
    gdc = Path(pc1gdcount_path)
    if not gdc.exists():
        write_file(pc1gdcount_path, "0")

def create_pc2_new_files(pc2gdcount_path, pc2gdstatus_path, pc2gmstatus_path):
    gdc = Path(pc2gdcount_path)
    if not gdc.exists():
        write_file(pc2gdcount_path, "0")

    gds = Path(pc2gdstatus_path)
    if not gds.exists():
        write_file(pc2gdstatus_path, "First run no status")

    gms = Path(pc2gmstatus_path)
    if not gms.exists():
        write_file(pc2gmstatus_path, "Unknown")
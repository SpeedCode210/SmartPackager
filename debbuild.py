#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : SpeedCode210
# version ='2.0'
# System dependencies : dpkg, fakeroot
# ---------------------------------------------------------------------------
"""Builds a DEB package from binaries"""
# ---------------------------------------------------------------------------

import config
import os
import regex

def __prepare_sources(source_name:str):
    path = f"/tmp/debbuild/{source_name}"
    os.system(f"mkdir -p {path}/usr/bin/{config.NAME}")
    os.system(f"mkdir -p {path}/usr/share/applications")
    os.system(f"cp -r {config.BASE_DIR}/* {path}/usr/bin/{config.NAME}/")
    os.system(f"mv {path}/usr/bin/{config.NAME}/*.desktop {path}/usr/share/applications")
    os.system(f"mkdir -p {path}/DEBIAN")
    os.system(f"cp {config.DEB_CONTROL_FILE} {path}/DEBIAN/control")
    
def __clean_files():
    os.system("rm -rf /tmp/debbuild/")

def __get_source_name():
    spec = open(config.DEB_CONTROL_FILE, "r").read()
    try:
        name = regex.findall("(?<=Package:\s*)[^\s]+?(?=\s*\\n)", spec)[0]
        version = regex.findall("(?<=Version:\s*)[^\s]+?(?=\s*\\n)", spec)[0]
    except:
        raise Exception("Invalid .spec file")
    return  f"{name}-{version}"

def generate_deb():
    try:
        print("-"*os.get_terminal_size().columns)
    except:
        print("-------------------------------------------")
    print("  SmartPackager - Building DEB Package")
    try:
        print("-"*os.get_terminal_size().columns)
    except:
        print("-------------------------------------------")
    source_name = __get_source_name()
    __prepare_sources(source_name)
    os.system(f"fakeroot sh -c 'cd /tmp/debbuild/ && dpkg-deb --build {source_name}'")
    os.system(f"cp /tmp/debbuild/*.deb {config.OUTPUT_FOLDER}")
    __clean_files()


if __name__ == "__main__":
    generate_deb()
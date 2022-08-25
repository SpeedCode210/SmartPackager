#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : SpeedCode210
# version ='2.0'
# System dependencies : rpmbuild, gzip, tar
# ---------------------------------------------------------------------------
"""Builds a RPM package from binaries"""
# ---------------------------------------------------------------------------

import config
import os
import regex

def __prepare_sources(source_name:str):
    path = f"/tmp/rpmbuild/{source_name}"
    os.system(f"mkdir -p {path}")
    os.system(f"cp -r {config.BASE_DIR}/* {path}")
    os.system(f"rm -f {config.RPM_SOURCES_FOLDER}/{source_name}.tar.gz")
    os.system(f"cd /tmp/rpmbuild/ && tar -czvf {config.RPM_SOURCES_FOLDER}/{source_name}.tar.gz {source_name}")
    
def __clean_files():
    os.system("rm -rf /tmp/rpmbuild/")

def __get_source_name():
    spec = open(config.RPM_SPEC_FILE, "r").read()
    try:
        name = regex.findall("(?<=Name:\s*)[^\s]+?(?=\s*\\n)", spec)[0]
        version = regex.findall("(?<=Version:\s*)[^\s]+?(?=\s*\\n)", spec)[0]
    except:
        raise Exception("Invalid .spec file")
    return  f"{name}-{version}"

def generate_rpm():
    try:
        print("-"*os.get_terminal_size().columns)
    except:
        print("-------------------------------------------")
    print("  SmartPackager - Building RPM Package")
    try:
        print("-"*os.get_terminal_size().columns)
    except:
        print("-------------------------------------------")
    source_name = __get_source_name()
    __prepare_sources(source_name)
    os.system(f"rpmbuild -ba {config.RPM_SPEC_FILE}")
    os.system(f"cp {config.RPM_RPMS_FOLDER}/*/{source_name}* {config.OUTPUT_FOLDER}")
    os.system(f"cp {config.RPM_SRPMS_FOLDER}/{source_name}* {config.OUTPUT_FOLDER}")
    __clean_files()


if __name__ == "__main__":
    generate_rpm()
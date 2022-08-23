#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : SpeedCode210
# version ='2.0'
# System dependencies : zip
# Pip dependencies : Pillow
# ---------------------------------------------------------------------------
"""Builds a SmartInstaller archive from windows binaries"""
# ---------------------------------------------------------------------------
import config
import os


def generate_smartinstaller():
    print("-"*os.get_terminal_size().columns)
    print("  SmartPackager - Building SmartInstaller archive")
    print("-"*os.get_terminal_size().columns)
    path = f"/tmp/smartinstaller"
    os.system(f"mkdir -p {path}/bin")
    os.system(f'cp -R {config.WIN_BASE_DIR}/* {path}/bin')
    os.system(f'cp {config.WIN_PKGJSON} {path}/package.json')
    os.system(f"sh -c 'cd {path} && zip -r /tmp/{config.NAME.lower()}-{config.VERSION}.zip ./'")
    os.system(f"cp /tmp/{config.NAME.lower()}-{config.VERSION}.zip {config.OUTPUT_FOLDER}")
    os.system(f"rm -rf {path}")


if __name__ == "__main__":
    generate_smartinstaller()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : SpeedCode210
# version ='2.0'
# System dependencies : tar, gzip
# Pip dependencies : Pillow
# ---------------------------------------------------------------------------
"""Builds a Flatpak source archive from binaries"""
# ---------------------------------------------------------------------------
import config
import os
from PIL import Image

def generate_flatpak_source():
    print("-"*os.get_terminal_size().columns)
    print("  SmartPackager - Building Flatpak sources archive")
    print("-"*os.get_terminal_size().columns)
    path = f"/tmp/flatpaksource"
    os.system(f"mkdir -p {path}")
    os.system(f'cp -R {config.BASE_DIR}/* {path}')
    if os.path.exists(f"{config.BASE_DIR}/App.png") :
        image = Image.open(f"{config.BASE_DIR}/App.png")
        new_image = image.resize((128, 128))
        new_image.save(f'{path}/128.png')
        new_image = image.resize((64, 64))
        new_image.save(f'{path}/64.png')
    os.system(f"sh -c 'cd {path} && tar -czvf /tmp/{config.NAME.lower()}-source-{config.VERSION}.tar.gz ./'")
    os.system(f"cp /tmp/{config.NAME.lower()}-source-{config.VERSION}.tar.gz {config.OUTPUT_FOLDER}")
    os.system(f"rm -rf {path}")


if __name__ == "__main__":
    generate_flatpak_source()
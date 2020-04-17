#!/usr/bin/env python

import os
from platform import system

from pathlib import WindowsPath, PosixPath

def read_file(file):
    with open(file, 'r', encoding = "utf-8") as file:
        return file.read()

def path_settings(directory):
    dest = os.getcwd()

    if system() == 'Windows':
        appdata = WindowsPath(os.getenv('APPDATA'))
        dest = appdata.joinpath(directory)
    else:
        dest = PosixPath('/etc').joinpath(directory)

    dest.mkdir(parents = True, exist_ok = True)

    return dest
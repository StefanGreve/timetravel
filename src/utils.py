#!/usr/bin/env python

import os
import json
import shutil
from platform import system

from pathlib import WindowsPath, PosixPath, Path

def read_file(file):
    with open(file, 'r', encoding = "utf-8") as file:
        return file.read()

def read_json(file):
    return json.loads(read_file(file))

def copy_settings(filename, project_name, overwrite = False):
    target_file= path_settings(project_name).joinpath(filename)

    if not target_file.exists() or (target_file.exists and overwrite):
        shutil.copy(
            Path.cwd().joinpath('src').joinpath(filename),
            target_file
        )

def path_settings(directory):
    dest = os.getcwd()

    if system() == 'Windows':
        appdata = WindowsPath(os.getenv('APPDATA'))
        dest = appdata.joinpath(directory)
    else:
        dest = PosixPath('/etc').joinpath(directory)

    dest.mkdir(parents = True, exist_ok = True)

    return dest

#!/usr/bin/env python

import os
from platform import system

from pathlib import Path

def path_settings(directory):
    dest = os.getcwd()

    if system() == 'Windows':
        appdata = Path(os.getenv('APPDATA'))
        dest = appdata.joinpath(directory)
    else:
        dest = PurePosixPath('/etc').joinpath(directory)

    dest.mkdir(parents = True, exist_ok = True)

    return dest
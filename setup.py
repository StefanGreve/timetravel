#!/usr/bin/env python

import json
import shutil
from setuptools import setup
from src import utils

from pathlib import Path

#region pre-setup procedures

settings = 'settings.json'
meta = 'meta.json'

utils.copy_settings(meta)
utils.copy_settings(settings)

metadata = None
with open(utils.path_settings('timetravel').joinpath(meta), encoding = "utf-8", mode = "r") as metadata:
        metadata = json.loads(metadata.read())

#endregion

setup(
    author = metadata['author'],
    keywords = "python cli collaboration",
    name = metadata['name'],
    version = metadata['version'],
    description = "Walltime utility script for collaboration.",
    long_description = utils.read_file("readme.md"),
    long_description_content_type = "text/markdown",
    url = "https://github.com/StefanGreve/timetravel",
    py_modules = [ "timetravel" ],
    package_dir = { '' : 'src' },
    install_requires = [
        'click',
        'colorama',
        'pathlib',
        'python-dateutil'
    ],

    python_requires=">=3.6.1",

    classifiers = [
        "Natural Language :: English",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ]
)
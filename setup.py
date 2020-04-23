#!/usr/bin/env python

import json
from setuptools import setup
from src import utils

from pathlib import Path

#region pre-setup procedures

META, SETTINGS, PROJECT = "meta.json", "settings.json", "timetravel"

utils.copy_settings(META, PROJECT)
utils.copy_settings(SETTINGS, PROJECT)

metadata = utils.read_json(utils.path_settings(PROJECT).joinpath(META))

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
    py_modules = [ PROJECT ],
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
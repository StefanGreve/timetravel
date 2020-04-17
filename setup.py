#!/usr/bin/env python

import shutil
from setuptools import setup
from src import utils

from pathlib import Path

# move settings file
settings = 'settings.json'
shutil.copy(
    Path.cwd().joinpath('src').joinpath(settings), 
    utils.path_settings('timetravel').joinpath(settings)
)

setup(
    author = "Stefan Greve",
    keywords = "python cli collaboration",
    name = 'timetravel',
    version = "1.1",
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
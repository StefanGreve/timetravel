# Time Travel

Time Travel is a CLI utility that helps you look up the current date and time
from your colleagues across the globe. Define a username as well as a region in
`settings.json` and you're good to go~

## Installation

```bash
    # enter project root, check wheel installation
    python -m pip install --user wheel
    # build wheel and install timetravel
    python setup.py bdist_wheel
    python -m pip install -r requirements.txt
```

## Basic Usage

```bash
    # show help message
    python timetravel.py --help
    # print all users from your settings
    python timetravel.py all
    # lookup current time
    python timetravel.py --user mazawa now
```

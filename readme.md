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
    python -m pip install --user -r requirements.txt
```

## Basic Usage

```bash
    # show help message
    python timetravel.py --help
    # print all users from your settings
    python timetravel.py all
    # lookup current time
    python timetravel.py --user mazawa time
```

## Notes

The user-defined configurations are stored in a JSON file. Once the project ran through `setup.py` a copy will be stored in

```bash
# windows
C:\Users\Stefan Greve\AppData\Roaming\timetravel\settings.json
# linux
etc/timetravel/settings.json
```

Changes to the configuration file should be made there, and not in `./src/settings.json`.

## TODO

- [ ] Implement a method that lets the user add a new entry to `settings.json` from the terminal. The available timezones are available in `pytz` as a list (currently not a project dependency); this is not very convenient, which is why I'd like to find a better solution for the `--city` option before I add this method.

```python
import pytz
print(pytz.all_timezones)
```

- [ ]  Add `--city` option as second (alternative) input for the `time` method. I have looked into this a little, and came up with a solution that would require a Google API Key. For example

```python
from faker import Faker
from geopy.geocoders import GoogleV3

def city_timezone(name):
    """ Translates name of city/address into a timezone. """
    google = GoogleV3(
        api_key = 'REDACTED',
        user_agent = Faker().user_agent()
    )
    return google.timezone(google.geocode(name).point)
```

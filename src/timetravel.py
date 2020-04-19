#!/usr/bin/env python3

import os
import json
import errno
from datetime import date, datetime
import utils

import click
from pathlib import Path
from dateutil.tz import gettz

def print_date_now(timezone):
    now = datetime.now().astimezone(gettz(timezone))
    click.echo(f"{click.style('[', fg = 'yellow')}{now.strftime('%Y-%m-%d')}{click.style(']', fg = 'yellow')} ", nl=False)
    click.echo(f"@ {click.style(now.strftime('%H:%M:%S'), fg = 'yellow')} ", nl = False)
    click.echo(f"in {click.style(timezone)}.")  

def print_version(ctx, param, value):
    meta = utils.path_settings('timetravel').joinpath('meta.json')
    meta_content = json.loads(utils.read_file(meta))
    
    if not value or ctx.resilient_parsing:
        return

    click.secho(f"Python {meta_content['name']} Version {meta_content['version']}", fg = 'yellow')
    click.echo(f"Copyright (C) {date.today().year} {meta_content['author']}")
    click.echo("License GPLv3: GNU GPL version 3 <https://gnu.org/licenses/gpl.html>")
    click.echo("This is free software: you are free to change and redistribute it.")
    click.echo("There is NO WARRANTY, to the extent permitted by law.")
    ctx.exit()

@click.group(invoke_without_command = True)
@click.option('--user', type = click.STRING, help = "Sets username as defined in settings.json")
@click.option('--city', type = click.STRING, help = "Derives timezone from city.")
@click.option('--version', is_flag = True, callback = print_version, expose_value = False, is_eager = True, help = "Display package version information.")
@click.pass_context
def cli(ctx, user, city):
    ctx.ensure_object(dict)
    ctx.obj['USER'] = user
    ctx.obj['CITY'] = city
    ctx.obj['SETTINGS'] = utils.path_settings('timetravel').joinpath('settings.json')

@cli.command()
@click.pass_context
def time(ctx):
    """ Prints current date and time of a specified user. """
    user = ctx.obj['USER']
    city = ctx.obj['CITY']
    settings = ctx.obj['SETTINGS']

    settings_content = json.loads(utils.read_file(settings))
    name = settings_content['name'].get(user, 'error')

    if city:
        raise NotImplementedError('You cannot use this option yet.')
    elif (user and name != 'error'):
        print_date_now(name['timezone'])        
    elif name == 'error':
        click.secho(f"Error Code {errno.EINVAL}: {os.strerror(errno.EINVAL)}", err = True, fg = 'red')
        click.secho(f"This user hasn't been defined in your settings yet.", fg = 'yellow')
        click.secho(f"You can add new users in '{utils.path_settings('timetravel')}'.", fg = 'yellow')
    else:
        click.secho(f"An unknown error has occurred", err = True, fg = 'red')


@cli.command()
@click.pass_context
def all(ctx):
    """ Reads and lists all users from settings. """
    settings = ctx.obj['SETTINGS']

    with open(settings, encoding = "utf-8", mode = "r") as settings:
        users = json.loads(settings.read())['name']

        for index, user in enumerate(users):
            click.secho(f"{(index+1):02}. ", fg = 'yellow', nl = False)
            click.echo(user)

 
if __name__ == '__main__':
    cli(obj = {})
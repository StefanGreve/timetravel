#!/usr/bin/env python3

import os
import json
import errno
from datetime import date, datetime
import utils

import click
from pathlib import Path
from dateutil.tz import gettz

def print_version(ctx, param, value):
    meta = utils.path_settings('timetravel').joinpath('meta.json')
    
    if not value or ctx.resilient_parsing:
        return
    with open(meta, encoding = "utf-8", mode = "r") as meta:
        meta = json.loads(meta.read())

        click.secho(f"Python {meta['name']} Version {meta['version']}", fg = 'yellow')
        click.echo(f"Copyright (C) {date.today().year} {meta['author']}")
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

    time = lambda tz: datetime.now().astimezone(gettz(tz))

    with open(settings, encoding = "utf-8", mode = "r") as settings:
        name = json.loads(settings.read())['name'].get(user, 'error')
        if city:
            raise NotImplementedError('You cannot use this option yet.')
        if name != 'error':
            user_tz = name['timezone']
            now = time(user_tz)
            click.echo(f"{click.style('[', fg = 'yellow')}{now.strftime('%Y-%m-%d')}{click.style(']', fg = 'yellow')} ", nl=False)
            click.echo(f"@ {click.style(now.strftime('%H:%M:%S'), fg = 'yellow')} ", nl = False)
            click.echo(f"in {click.style(user_tz)}.")  
        else:
            click.secho(f"Error Code {errno.EINVAL}: {os.strerror(errno.EINVAL)}", err = True, fg = 'red')
            click.secho(f"This user hasn't been defined in your settings yet.", fg = 'yellow')
            click.secho(f"You can add new users in '{utils.path_settings('timetravel')}'.", fg = 'yellow')


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
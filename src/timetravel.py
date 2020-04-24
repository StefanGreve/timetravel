#!/usr/bin/env python3

import os
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
    meta = utils.read_json(utils.path_settings('timetravel').joinpath('meta.json'))
    
    if not value or ctx.resilient_parsing:
        return

    click.secho(f"\nPython {meta['name']} version {meta['version']}", fg = 'yellow')
    click.echo(f"Copyright (C) {date.today().year} {meta['author']}")
    click.echo("License GPLv3: GNU GPL version 3 <https://gnu.org/licenses/gpl.html>")
    click.echo("This is free software: you are free to change and redistribute it.")
    click.echo("There is NO WARRANTY, to the extent permitted by law.\n")
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
    user = ctx.obj['USER']
    city = ctx.obj['CITY']

    name = utils.read_json(ctx.obj['SETTINGS'])['name'].get(user, 'error')

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
    users = utils.read_json(ctx.obj['SETTINGS'])['name']

    for index, user in enumerate(users):
        click.secho(f"{(index+1):02}. ", fg = 'yellow', nl = False)
        click.echo(user)

 
if __name__ == '__main__':
    try:
        cli(obj = {})
    except KeyboardInterrupt:
        pass
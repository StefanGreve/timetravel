#!/usr/bin/env python3

import json
from datetime import date, datetime
import utils

import click
from pathlib import Path
from dateutil.tz import gettz

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.secho(f"Python Timetravel Version {'1.1'}", fg = 'yellow')
    click.echo(f"Copyright (C) {date.today().year} Stefan Greve")
    click.echo("License GPLv3: GNU GPL version 3 <https://gnu.org/licenses/gpl.html>")
    click.echo("This is free software: you are free to change and redistribute it.")
    click.echo("There is NO WARRANTY, to the extent permitted by law.")
    ctx.exit()

@click.group(invoke_without_command = True)
@click.option('--user', type = click.STRING, help = "Set username as defined in settings.json")
@click.option('--version', is_flag = True, callback = print_version, expose_value = False, is_eager = True, help = "Display package version information.")
@click.pass_context
def cli(ctx, user):
    ctx.ensure_object(dict)
    ctx.obj['USER'] = user
    ctx.obj['SETTINGS'] = utils.path_settings('timetravel').joinpath('settings.json')

@cli.command()
@click.pass_context
def time(ctx):
    """ Prints current date and time of a specified user. """
    user = ctx.obj['USER']
    settings = ctx.obj['SETTINGS']

    with open(settings, encoding = "utf-8", mode = "r") as settings:
        user_tz = json.loads(settings.read())['name'][user]['timezone']
        now = datetime.now().astimezone(gettz(user_tz))
        # print into respective timezone translated datetime
        click.echo(f"{click.style('[', fg = 'yellow')}{now.strftime('%Y-%m-%d')}{click.style(']', fg = 'yellow')} ", nl=False)
        click.echo(f"@ {click.style(now.strftime('%H:%M:%S'), fg = 'yellow')} ", nl = False)
        click.echo(f"in {click.style(user_tz)}.")  


@cli.command()
@click.pass_context
def all(ctx):
    """ Reads and lists all users from settings. """
    settings = ctx.obj['SETTINGS']

    with open(settings, encoding = "utf-8", mode = "r") as settings:
        users = json.loads(settings.read())['name']

        for index, user in enumerate(users):
            click.secho(f"{(index+1):02}. ", fg = 'yellow', nl = False)
            click.secho(user)

 
if __name__ == '__main__':
    cli(obj = {})
#!/usr/bin/env python

import json
from datetime import datetime
import utils

import click
from pathlib import Path
from dateutil.tz import gettz

@click.group(invoke_without_command = True)
@click.option('--user', type = click.STRING, help = "The username as defined in settings.json")
@click.pass_context
def cli(ctx, user):
    ctx.ensure_object(dict)
    ctx.obj['USER'] = user
    ctx.obj['SETTINGS'] = utils.path_settings('timetravel').joinpath('settings.json')

@cli.command()
@click.pass_context
def now(ctx):
    """ Prints current date and time of a specified user. """
    user = ctx.obj['USER']
    settings = ctx.obj['SETTINGS']

    with open(settings, encoding = "utf-8", mode = "r") as settings:
        # retrieve user timezone from settings
        user_tz = json.loads(settings.read())['name'][user]['timezone']
        now = datetime.now().astimezone(gettz(user_tz))
        # display into respective timezone translated datetime
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
            click.secho(f"{(index+1):02}. {user}", fg = 'yellow')

 
if __name__ == '__main__':
    cli(obj = {})
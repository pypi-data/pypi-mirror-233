import click
from pathlib import Path
import tomllib
import os
import time
import numpy as np

#  ──────────────────────────────────────────────────────────────────────────
# base command

@click.group(invoke_without_command=True)
@click.option('-c', '--config', default='~/.config/dlog.toml', type=str, help="Config file path", show_default=True)
@click.pass_context
def dlog(ctx, config):
    ctx.ensure_object(dict)

    config = Path(config).expanduser()
    if config.exists():

        with open(config, 'rb') as file:
            toml = tomllib.load(file)

        # required config options
        required = ['logs']
        for option in required:
            if option not in toml:
                click.echo('Config requires "' + key + '" to be set.')
                exit()

        # home log directory
        if 'home' in toml:
            ctx.obj['home'] = Path(toml['home']).expanduser()
        else:
            ctx.obj['home'] = Path('~/dlogs').expanduser()

        # individual logs
        ctx.obj['logs'] = []
        for log in toml['logs']:
            ctx.obj['logs'].append(log)

            log_path = ctx.obj['home'] / Path(log)

            if not log_path.exists():
                os.mkdir(log_path)

        # editor
        if 'editor' in toml:
            ctx.obj['editor'] = toml['editor']
        else:
            ctx.obj['editor'] = 'vim'

    else:
        click.echo('No config file, exiting.')
        exit()

#  ──────────────────────────────────────────────────────────────────────────
# log command to generate single logs

@dlog.command()
@click.argument('name', type=str)
@click.pass_context
def log(ctx, name):

    if name in ctx.obj['logs']:
        log_path = ctx.obj['home'] / Path(name)

        epoch = str(np.floor(time.time()).astype(np.int64))
        date = time.strftime("%a, %d %b %Y %H:%M:%S UTC", time.gmtime())

        file_path = log_path / Path(epoch + '.md')
        with open(file_path, 'a') as file:
            file.write('# ' + date + '\n')

        click.edit(filename=file_path, editor=ctx.obj['editor'])

    else:
        click.echo(name + ' log not found in config.')
        exit()


#MIT License
#
#Copyright (c) 2022-2023 DevOps117
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


import logging # logging.basicConfig, logging.DEBUG, logging.INFO
import typing # typing.TextIO

import click # click.command, click.option, click.File, click.Path
import pyrogram # pyrogram.compose

import pyrocatto_bot # __version__
from .client_builder import ClientConfig, ClientBuilder


@click.group()
def start_bot() -> None:
    pass

@start_bot.command()
@click.option('--session-dir', required=True, type=click.Path(exists=True, readable=True, file_okay=False, dir_okay=True))
@click.option('--config', required=True, type=click.File(mode='r'))
@click.option('--debug', is_flag=True, default=False)
def start(session_dir: str, config: typing.TextIO, debug: bool) -> None:
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    client_configs = ClientConfig.from_yaml(config)
    client_builders = map(ClientBuilder, client_configs)
    pyrogram.compose(client_builder.create_client(session_dir) for client_builder in client_builders)

@start_bot.command()
def version() -> None:
    click.echo(pyrocatto_bot.__version__)


if __name__ == "__main__":
    start_bot()

__all__ = [""]

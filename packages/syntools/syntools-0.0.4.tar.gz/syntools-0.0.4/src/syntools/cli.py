import os
import argparse
import asyncio
import sys
from signal import SIGINT, SIGTERM
from ._version import __version__
from .commands.find_id import cli as find_id_cli
from .commands.sync import cli as sync_cli
from .commands.compare import cli as compare_cli
from .commands.copy import cli as copy_cli
from .commands.move import cli as move_cli
from .commands.invite_to_team import cli as invite_to_team_cli
from .commands.list import cli as list_cli
from .commands.download import cli as download_cli
from .core import Logging
from synapsis import cli as synapsis_cli, Synapsis

ALL_COMMANDS = [download_cli, sync_cli, find_id_cli, copy_cli, move_cli, invite_to_team_cli, list_cli, compare_cli]
# TODO: Delete these two lines once all the commands are working and tested.
ACTIVE_COMMANDS = [download_cli, find_id_cli, copy_cli, move_cli, list_cli]
ALL_COMMANDS = ACTIVE_COMMANDS


def __on_after_login__(hook):
    for name, default, attr in [
        ('SYNTOOLS_MULTI_THREADED', 'False', 'multi_threaded'),
        ('SYNTOOLS_USE_BOTO_STS_TRANSFERS', 'False', 'use_boto_sts_transfers')
    ]:
        env_value = os.environ.get(name, default).lower() == 'true'
        setattr(Synapsis.Synapse, attr, env_value)
        if env_value:
            Logging.info('Setting {0}={1}'.format(attr, env_value))


def __init__hooks__():
    Synapsis.hooks.after_login(__on_after_login__)


def main():
    shared_parser = argparse.ArgumentParser(add_help=False)
    synapsis_cli.inject(shared_parser)

    shared_parser.add_argument('-ll', '--log-level', help='Set the logging level.', default='INFO')
    shared_parser.add_argument('-ld', '--log-dir', help='Set the directory where the log file will be written.')
    main_parser = argparse.ArgumentParser(description='Synapse Power Tools')
    main_parser.add_argument('--version', action='version', version='%(prog)s {0}'.format(__version__))

    subparsers = main_parser.add_subparsers(title='Commands', dest='command')
    for command in ALL_COMMANDS:
        command.create(subparsers, [shared_parser])

    cmd_args = main_parser.parse_args()

    Logging.configure(log_dir=cmd_args.log_dir, log_level=cmd_args.log_level)

    if '_execute' in cmd_args:
        __init__hooks__()
        synapsis_cli.configure(cmd_args, login=True)
        loop = asyncio.get_event_loop()
        task = asyncio.ensure_future(cmd_args._execute(cmd_args))

        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        else:
            for signal in [SIGINT, SIGTERM]:
                loop.add_signal_handler(signal, task.cancel)
        try:
            loop.run_until_complete(task)
        finally:
            loop.close()
    else:
        main_parser.print_help()

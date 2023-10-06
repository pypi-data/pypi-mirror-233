# Copyright 2022 Scott K Logan
# Licensed under the Apache License, Version 2.0

from collections import OrderedDict
import os

from colcon_core.command import add_subparsers
from colcon_core.command import CommandContext
from colcon_core.command import create_parser
from colcon_core.command import verb_main
from colcon_core.extension_point \
    import EXTENSION_BLOCKLIST_ENVIRONMENT_VARIABLE
from colcon_core.logging import colcon_logger
from colcon_core.plugin_system import satisfies_version
from colcon_core.verb import get_verb_extensions
from colcon_core.verb import VerbExtensionPoint
from colcon_rerun.config import get_config

logger = colcon_logger.getChild(__name__)


def _disable_capture():
    blocklist = os.environ.get(
        EXTENSION_BLOCKLIST_ENVIRONMENT_VARIABLE.name, '')
    if blocklist:
        blocklist += os.pathsep
    blocklist += 'colcon_core.argument_parser.rerun'
    os.environ[EXTENSION_BLOCKLIST_ENVIRONMENT_VARIABLE.name] = blocklist


def _invoke_verb(command_name, verb_name, argv):
    print(
        'Re-running previous command: {} {}'.format(
            command_name, ' '.join(argv)))

    parser = create_parser('colcon_core.environment_variable')
    verb_extensions = OrderedDict(
        pair for pair in get_verb_extensions().items()
        if pair[0] == verb_name)
    if verb_extensions:
        add_subparsers(
            parser, command_name, verb_extensions, attribute='verb_name')

    args = parser.parse_args(args=argv)
    context = CommandContext(command_name=command_name, args=args)

    return verb_main(context, colcon_logger)


class ReRunVerb(VerbExtensionPoint):
    """Quickly re-run a recently executed verb."""

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(VerbExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')

    def add_arguments(self, *, parser):  # noqa: D102
        parser.add_argument(
            'verb_to_run', nargs='?',
            help='The verb to re-run (default: most recent verb)')
        parser.add_argument(
            'additional_args', nargs='*', type=str.lstrip, default=[],
            help='Additional arguments to pass to the command')

    def main(self, *, context):  # noqa: D102
        config_content = get_config()

        if not context.args.verb_to_run:
            context.args.verb_to_run = config_content.get('last_verb')
            if not context.args.verb_to_run:
                raise RuntimeError(
                    'No previously recorded invocation to re-run')

        _disable_capture()

        argv = config_content.get('full_captures', {}).get(
            context.args.verb_to_run, [context.args.verb_to_run])
        argv += context.args.additional_args
        return _invoke_verb(
            context.command_name, context.args.verb_to_run, argv)

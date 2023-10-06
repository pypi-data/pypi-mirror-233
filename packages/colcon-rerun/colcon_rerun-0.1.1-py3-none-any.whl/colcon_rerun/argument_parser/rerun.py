# Copyright 2022 Scott K Logan
# Licensed under the Apache License, Version 2.0

import sys

from colcon_core.argument_parser import ArgumentParserDecorator
from colcon_core.argument_parser import ArgumentParserDecoratorExtensionPoint
from colcon_core.logging import colcon_logger
from colcon_core.plugin_system import satisfies_version
from colcon_rerun.config import update_config

logger = colcon_logger.getChild(__name__)


class ReRunArgumentParserDecorator(ArgumentParserDecoratorExtensionPoint):
    """Capture arguments for recently executed verbs."""

    # High priority to capture the arguments as they were passed,
    # before being modified by other parsers
    PRIORITY = 500

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(
            ArgumentParserDecoratorExtensionPoint.EXTENSION_POINT_VERSION,
            '^1.0')

    def decorate_argument_parser(self, *, parser):  # noqa: D102
        return ReRunArgumentDecorator(parser)


class ReRunArgumentDecorator(ArgumentParserDecorator):
    """Capture arguments for recently executed verbs."""

    def parse_args(self, *args, **kwargs):  # noqa: D102
        parsed_args = self._parser.parse_args(*args, **kwargs)
        if getattr(parsed_args, 'verb_name', None) not in (None, 'rerun'):
            raw_args = kwargs.get('args')
            if not raw_args:
                if args:
                    raw_args = args[0]
                else:
                    raw_args = sys.argv[1:]
            update_config(parsed_args.verb_name, raw_args)
        return parsed_args

# Copyright 2022 Scott K Logan
# Licensed under the Apache License, Version 2.0

from colcon_core.location import get_config_path
from colcon_rerun import CONFIG_NAME
from colcon_rerun.logging import configure_filelock_logger
import filelock
import yaml


def get_config():
    """Get the global colcon-rerun configuration."""
    configure_filelock_logger()

    config_path = get_config_path()
    config_path.mkdir(parents=True, exist_ok=True)
    config_file = config_path / CONFIG_NAME
    lock_file = config_path / '.{}.lock'.format(CONFIG_NAME)
    try:
        with filelock.FileLock(lock_file, timeout=5):
            with config_file.open() as f:
                return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


def update_config(verb_name, commands):
    """Update the global colcon-rerun configuration."""
    configure_filelock_logger()

    config_path = get_config_path()
    config_path.mkdir(parents=True, exist_ok=True)
    config_file = config_path / CONFIG_NAME
    lock_file = config_path / '.{}.lock'.format(CONFIG_NAME)
    with filelock.FileLock(lock_file, timeout=5):
        with config_file.open('a+') as f:
            f.seek(0)
            config = yaml.safe_load(f) or {}
            config.setdefault('full_captures', {})
            if (
                config['full_captures'].get(verb_name, []) == commands and
                config.get('last_verb') == verb_name
            ):
                return
            config['full_captures'][verb_name] = commands
            config['last_verb'] = verb_name
            f.seek(0)
            f.truncate()
            yaml.dump(config, f, default_style="'")

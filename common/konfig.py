# SPDX-FileCopyrightText: © 2024 Christian BUHTZ <c.buhtz@posteo.jp>
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This file is part of the program "Back In time" which is released under GNU
# General Public License v2 (GPLv2).
# See file LICENSE or go to <https://www.gnu.org/licenses/#GPL>.
from __future__ import annotations
import os
import configparser
import inspect
from typing import Union, Any
from pathlib import Path
from io import StringIO
import singleton
import logger


def _attr_by_caller() -> str:
    """The name of the calling method is transformed into an config file attribute name.

    It is a helper function used `Konfig` and `Konfig.Profile` class.

    Returns:
        The attribute name.
    """

    # e.g. "hash_collision" if called from "Konfig.hash_collision" property
    method_name = inspect.currentframe().f_back.f_code.co_name

    # e.g. "hash_collision" -> "hash.collision"
    return method_name.replace('_', '.')


class Konfig(metaclass=singleton.Singleton):
    """Manage configuration of Back In Time.

    That class is a replacement for the `config.Config` class.
    """
    class Profile:
        def __init__(self, profile_id: int, config: Konfig):
            self._config = config
            self._prefix = f'profile{profile_id}'

        def __getitem__(self, key: str):
            try:
                return self._config[f'{self._prefix}.{key}']
            except KeyError as exc:
                # RETURN DEFAULT
                raise exc

        def _value_by_property_name(self) -> Any:
            """Return the value based on the calling property method."""
            attr_name = foobar()
            # method_name = inspect.currentframe().f_back.f_code.co_name
            # attr_name = method_name.replace('_', '.')

            return self[attr_name]

        @property
        def snapshots_mode(self):
            """Use mode (or backend) for this snapshot. Look at 'man
            backintime' section 'Modes'.

            {
               'values': 'local|local_encfs|ssh|ssh_encfs',
               'default': 'local',
            }
            """
            return self['snapshots.mode']
            # return self._value_by_property_name()

        @property
        def snapshots_path(self):
            """Where to save snapshots in mode 'local'. This path must contain
            a folderstructure like 'backintime/<HOST>/<USER>/<PROFILE_ID>'.

            {
                'values': 'absolute path',
            }
            """
            return self._value_by_property_name()

    _DEFAULT_SECTION = '[bit]'

    def __init__(self, config_path: Path = None):
        """
        """
        if not config_path:
            xdg_config = os.environ.get('XDG_CONFIG_HOME',
                                        os.environ['HOME'] + '/.config')
            self._path = Path(xdg_config) / 'backintime' / 'config'

        logger.debug(f'Config path used: {self._path}')

        self.load()

        # Names and IDs of profiles
        name_items = filter(
            lambda val:
                val[0].startswith('profile') and val[0].endswith('name'),
            self._conf.items()
        )
        self._profiles = {
            name: int(pid.replace('profile', '').replace('.name', ''))
            for pid, name in name_items
        }
        # # First/Default profile not stored with name
        # self._profiles[1] = _('Main profile')

    def __getitem__(self, key: str):
        return self._conf[key]

    def profile(self, name_or_id: Union[str, int]) -> Profile:
        if isinstance(name_or_id, int):
            profile_id = name_or_id
        else:
            profile_id = self._profiles[name_or_id]

        return self.Profile(profile_id=profile_id, config=self)

    @property
    def profile_names(self) -> list[str]:
        return list(self._profiles.keys())

    @property
    def profile_ids(self) -> list[int]:
        return list(self._profiles.values())

    def load(self):
        self._config_parser = configparser.ConfigParser(
            defaults={'profile1.name': _('Main profile')})

        with self._path.open('r', encoding='utf-8') as handle:
            content = handle.read()
            logger.debug(f'Configuration read from "{self._path}".')

        # Add section header to make it a real INI file
        self._config_parser.read_string(f'{self._DEFAULT_SECTION}\n{content}')

        # The one and only main section
        self._conf = self._config_parser['bit']

    def save(self):
        buffer = StringIO()
        self._config_parser.write(buffer)
        buffer.seek(0)

        with self._path.open('w', encoding='utf-8') as handle:
            # Write to file without section header
            handle.write(''.join(buffer.readlines()[1:]))
            logger.debug(f'Configuration written to "{self._path}".')

    @property
    def hash_collision(self) -> int:
        """Internal value used to prevent hash collisions on mountpoints.
        Do not change this.

        {
            'values': (0, 99999),
            'default': 0,
        }
        """
        return self._conf['global.hash_collision']

    @property
    def language(self) -> str:
        """Language code (ISO 639) used to translate the user interface. If
        empty the operating systems current local is used. If 'en' the
        translation is not active and the original English source strings are
        used. It is the same if the value is unknown.
        {
            'values': 'ISO 639 language codes'
        }
        """
        return self._conf['global.language']



if __name__ == '__main__':
    # Workaround because of missing gettext config
    _ = lambda s: s

    k = Konfig()
    print(f'{k._conf.keys()=}')

    print(f'{k.profile_names=}')
    print(f'{k.profile_ids=}')
    print(f'{k.global_hash_collision=}')
    p = k.profile(2)
    print(f'{p.snapshots_mode=}')

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


class Konfig(metaclass=singleton.Singleton):
    """Manage configuration of Back In Time.

    That class is a replacement for the `config.Config` class.
    """
    class Profile:
        DEFAULT_VALUES = {
            'snapshots.ssh.port': 22,
        }

        def __init__(self, profile_id: int, config: Konfig):
            self._config = config
            self._prefix = f'profile{profile_id}'

        def __getitem__(self, key: str):
            try:
                return self._config[f'{self._prefix}.{key}']
            except KeyError as exc:
                return self.DEFAULT_VALUES[key]

        @property
        def snapshots_mode(self) -> str:
            """Use mode (or backend) for this snapshot. Look at 'man
            backintime' section 'Modes'.

            {
               'values': 'local|local_encfs|ssh|ssh_encfs',
               'default': 'local',
            }
            """
            return self['snapshots.mode']

        @property
        def snapshots_path(self) -> str:
            """Where to save snapshots in mode 'local'. This path must contain
            a folderstructure like 'backintime/<HOST>/<USER>/<PROFILE_ID>'.

            {
                'values': 'absolute path',
                'type': str,
            }
            """
            raise NotImplementedError('see original in Config class')
            return self['snapshots.path']

        @property
        def ssh_snapshots_path(self) -> str:
            """Snapshot path on remote host. If the path is relative (no
            leading '/') it will start from remote Users homedir. An empty path
            will be replaced with './'.

            {
                'values': 'absolute or relative path',
                'type': str,
            }

            """
            return self['snapshots.ssh.path']

        @property
        def ssh_host(self):
            """Remote host used for mode 'ssh' and 'ssh_encfs'.

            {
                'values': 'IP or domain address',
            }
            """
            return self['snapshots.ssh.host']

        @ssh_host.setter
        def ssh_host(self, value: str) -> None:
            self['snapshots.ssh.host'] = value

        @property
        def ssh_port(self) -> str:
            """SSH Port on remote host.

            {
                'values': '0-65535',
                'default': 22,
            }
            """
            return self['snapshots.ssh.port']

        @ssh_port.setter
        def ssh_port(self, value: int) -> None:
            self['snapshots.ssh.port'] = value


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

    def __getitem__(self, key: str) -> Any:
        return self._conf[key]

    def __setitem__(self, key: str, val: Any) -> None:
        self._conf[key] = val

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
        return self['global.hash_collision']

    @hash_collision.setter
    def hash_collision(self, val: int) -> None:
        self['global.hash_collision'] = val

    @property
    def language(self) -> str:
        """Language code (ISO 639) used to translate the user interface. If
        empty the operating systems current local is used. If 'en' the
        translation is not active and the original English source strings are
        used. It is the same if the value is unknown.
        {
            'values': 'ISO 639 language codes',
            'type': str
        }
        """
        return self['global.language']

    @language.setter
    def language(self, lang: str) -> None:
        self['global.language'] = lang

    @property
    def global_flock(self) -> bool:
        """Prevent multiple snapshots (from different profiles or users) to be
        run at the same time.
        {
            'values': 'true|false',
            'default': 'false',
            'type': bool
        }
        """
        return self['global.use_flock']

    @global_flock.setter
    def global_flock(self, value: bool) -> None:
        self['global.use_flock'] = value


if __name__ == '__main__':
    # Workaround because of missing gettext config
    _ = lambda s: s

    k = Konfig()

    print(f'{k.profile_names=}')
    print(f'{k.profile_ids=}')
    print(f'{k.hash_collision=}')
    print(f'{k.language=}')
    print(f'{k.global_flock=}')

    p = k.profile(2)
    print(f'{p.snapshots_mode=}')

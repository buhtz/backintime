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
from typing import Union
from pathlib import Path
from io import StringIO
import singleton
import logger


class Konfig(metaclass=singleton.Singleton):
    """Manage configuration of Back In Time.

    That class is a replacement for the `config.Config` class.
    """
    # use with ConfigParser(defaults=_DEFAULT)
    # _DEFAULT = {
    #     'foo': 7,
    #     'bar': 'bähm',
    #     'profiles': '24842'
    # }

    # class _AttrSection:
    #     def __init__(self,
    #                  name: str,
    #                  parent: _AttrSection,
    #                  section: configparser.SectionProxy):
    #         self._name = name
    #         self._parent = parent
    #         self._section = section

    #     def full_attr_name(self) -> str:
    #         return f'{self.parent.full_attr_name}.{self._name}'

    #     def __getattr__(self, attr: str):
    #         if '.' in attr:
    #             attr_section = _AttrSection(
    #                 name=attr, parent=self, section=self._section)
    #             return attr_section[attr]

    #         return self._conf[attr]

    class Profile:
        def __init__(self, profile_id: int, config: Konfig):
            self._config = config
            self._prefix = f'profile{profile_id}'

        def __getitem__(self, key: str):
            return self._config[f'{self._prefix}.{key}']

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
        "bar"
        return list(self._profiles.keys())

    @profile_names.setter
    def profile_names(self, val):
        """boom"""
        pass

    @property
    def profile_ids(self) -> list[int]:
        """foo"""
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


if __name__ == '__main__':
    _ = lambda s: s
    k = Konfig()

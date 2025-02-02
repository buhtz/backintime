# SPDX-FileCopyrightText: © 2024 Christian BUHTZ <c.buhtz@posteo.jp>
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This file is part of the program "Back In time" which is released under GNU
# General Public License v2 (GPLv2). See file/folder LICENSE or go to
# <https://spdx.org/licenses/GPL-2.0-or-later.html>.
"""Basic constants used in multiple modules."""
from enum import Enum
from pathlib import Path

# Workaround: Mostly relevant on TravisCI but not exclusively.
# While unittesting and without regular invocation of BIT the GNU gettext
# class-based API isn't setup yet.
# pylint: disable=duplicate-code
try:
    _('Warning')
except NameError:
    def _(val):
        return val

# See issue #1734 and #1735
URL_ENCRYPT_TRANSITION = 'https://github.com/bit-team/backintime' \
                         '/blob/-/doc/ENCRYPT_TRANSITION.md'

SSH_CIPHERS = {
    'default': _('Default'),
    'aes128-ctr': 'AES128-CTR',
    'aes192-ctr': 'AES192-CTR',
    'aes256-ctr': 'AES256-CTR',
    'arcfour256': 'ARCFOUR256',
    'arcfour128': 'ARCFOUR128',
    'aes128-cbc': 'AES128-CBC',
    '3des-cbc': '3DES-CBC',
    'blowfish-cbc': 'Blowfish-CBC',
    'cast128-cbc': 'Cast128-CBC',
    'aes192-cbc': 'AES192-CBC',
    'aes256-cbc': 'AES256-CBC',
    'arcfour': 'ARCFOUR'
}

USER_MANUAL_ONLINE_URL = 'https://backintime.readthedocs.io'
USER_MANUAL_LOCAL_PATH = Path('/') / 'usr' / 'share' / 'doc' / \
    'backintime-common' / 'manual' / 'index.html'
USER_MANUAL_LOCAL_AVAILABLE = USER_MANUAL_LOCAL_PATH.exists()


class TimeUnit(Enum):
    """Describe time units used in context of scheduling."""
    HOUR = 10  # Config.HOUR
    DAY = 20  # Config.DAY
    WEEK = 30  # Config.WEEK
    MONTH = 40  # Config.MONTH
    YEAR = 80  # Config.Year


class StorageSizeUnit(Enum):
    """Describe the units used to express the size of storage devices or file
    system objects."""
    MB = 10  # Config.DISK_UNIT_MB
    GB = 20  # Config.DISK_UNIT_GB

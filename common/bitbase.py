# SPDX-FileCopyrightText: © 2024 Christian BUHTZ <c.buhtz@posteo.jp>
#
# SPDX-License-Identifier: GPL-2.0
#
# This file is part of the program "Back In time" which is released under GNU
# General Public License v2 (GPLv2).
# See file LICENSE or go to <https://www.gnu.org/licenses/#GPL>.
"""Basic constants used in multiple modules."""

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

# SPDX-FileCopyrightText: © 2024 Christian BUHTZ <c.buhtz@posteo.jp>
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This file is part of the program "Back In Time" which is released under GNU
# General Public License v2 (GPLv2).
# See file LICENSE or go to <https://www.gnu.org/licenses/#GPL>.
import unittest
from io import StringIO
from konfig import Konfig


class General(unittest.TestCase):
    """Konfig class"""
    def test_empty(self):
        """Empty config file"""
        sut = Konfig(StringIO(''))

        self.assertEqual(
            dict(sut._conf.items()),
            {'profile1.name': 'Main profile'}
        )

    def test_default_values(self):
        """Default values and their types of fields if not present."""
        sut = Konfig(StringIO(''))

        self.assertEqual(sut.global_flock, False)
        self.assertIsInstance(sut.global_flock, bool)
        self.assertEqual(sut.language, '')
        self.assertIsInstance(sut.language, str)
        self.assertEqual(sut.hash_collision, 0)
        self.assertIsInstance(sut.hash_collision, int)


class Profiles(unittest.TestCase):
    """Konfig.Profile class"""
    def test_empty(self):
        """Profile child objects"""
        konf = Konfig(StringIO(''))
        sut = konf.profile(1)
        self.assertEqual(sut['name'], 'Main profile')

    def test_default_values(self):
        """Default values and their types of fields if not present."""
        sut = Konfig(StringIO('')).profile(0)

        self.assertEqual(sut.ssh_check_commands, True)
        self.assertIsInstance(sut.ssh_check_commands, bool)
        self.assertEqual(sut.ssh_cipher, 'default')
        self.assertIsInstance(sut.ssh_cipher, str)
        self.assertEqual(sut.ssh_port, 22)
        self.assertIsInstance(sut.ssh_port, int)

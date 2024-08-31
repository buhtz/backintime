# SPDX-FileCopyrightText: © 2024 Christian BUHTZ <c.buhtz@posteo.jp>
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This file is part of the program "Back In Time" which is released under GNU
# General Public License v2 (GPLv2).
# See file LICENSE or go to <https://www.gnu.org/licenses/#GPL>.
import unittest
import configparser
import pyfakefs.fake_filesystem_unittest as pyfakefs_ut
from pathlib import Path
from io import StringIO
from konfig import Konfig


class General(unittest.TestCase):
    """Konfig class"""

    def setUp(self):
        Konfig._instances = {}

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

    def test_no_interpolation(self):
        """Interpolation should be turned off"""
        try:
            Konfig(StringIO('qt.diff.params=%6 %1 %2'))
        except configparser.InterpolationSyntaxError as exc:
            self.fail(f'InterpolationSyntaxError was raised. {exc}')


class Read(unittest.TestCase):
    """Read a config file/object"""

    def setUp(self):
        Konfig._instances = {}

    def test_from_memory_via_ctor(self):
        """Config in memory"""
        buffer = StringIO('global.language=xz')
        sut = Konfig(buffer)

        self.assertEqual(sut.language, 'xz')

    def test_from_memory_via_load(self):
        """Config in memory"""
        sut = Konfig()
        self.assertEqual(sut.language, '')

        buffer = StringIO('global.language=ab')
        sut.load(buffer)
        self.assertEqual(sut.language, 'ab')

    @pyfakefs_ut.patchfs
    def test_from_file_via_ctor(self, fake_fs):
        """Config in from file"""
        fp = Path.cwd() / 'file'
        with fp.open('w', encoding='utf-8') as handle:
            handle.write('global.language=rt\n')

        with fp.open('r', encoding='utf-8') as handle:
            sut = Konfig(handle)
        self.assertEqual(sut.language, 'rt')

    @pyfakefs_ut.patchfs
    def test_from_file_via_load(self, fake_fs):
        """Config in from file"""
        sut = Konfig()
        self.assertEqual(sut.language, '')

        fp = Path.cwd() / 'filezwei'
        with fp.open('w', encoding='utf-8') as handle:
            handle.write('global.language=wq\n')

        with fp.open('r', encoding='utf-8') as handle:
            sut.load(handle)
        self.assertEqual(sut.language, 'wq')


class Profiles(unittest.TestCase):
    """Konfig.Profile class"""

    def setUp(self):
        Konfig._instances = {}

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

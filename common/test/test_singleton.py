# SPDX-FileCopyrightText: © 2024 Christian BUHTZ <c.buhtz@posteo.jp>
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This file is part of the program "Back In time" which is released under GNU
# General Public License v2 (GPLv2).
# See file LICENSE or go to <https://www.gnu.org/licenses/#GPL>.
import unittest
import singleton


class Test(unittest.TestCase):
    class Foo(metaclass=singleton.Singleton):
        def __init__(self):
            self.value = 'Ogawa'

    class Bar(metaclass=singleton.Singleton):
        def __init__(self):
            self.value = 'Naomi'

    def setUp(self):
        # Clean up all instances
        Singleton._instances = {}

    def test_twins(self):
        """Identical id and values."""
        a = Foo()
        b = Foo()

        self.assertEqual(id(a), id(b))
        self.assertEqual(a.value, b.value)

    def test_share_value(self):
        """Modify value"""
        a = Foo()
        b = Foo()
        a.value = 'foobar'

        self.assertEqual(a.value, 'foobar')
        self.assertEqual(a.value, b.value)

    def test_multi_class(self):
        """Two different singleton classes."""
        a = Foo()
        b = Foo()
        x = Bar()
        y = Bar()

        self.assertEqual(id(a), id(b))
        self.assertEqual(id(x), id(y))
        self.assertNotEqual(id(a), id(y))

        self.assertEqual(a.value, 'Ogawa')
        self.assertEqual(x.value, 'Naomi')

        a.value = 'who'
        self.assertEqual(b.value, 'who')
        self.assertEqual(x.value, 'Naomi')
        self.assertEqual(x.value, y.value)

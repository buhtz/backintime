# SPDX-FileCopyrightText: © 2024 Christian BUHTZ <c.buhtz@posteo.jp>
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This file is part of the program "Back In time" which is released under GNU
# General Public License v2 (GPLv2).
# See file LICENSE or go to <https://www.gnu.org/licenses/#GPL>.

class Konfig:
    """Manage configuration of Back In Time.

    That class is a replacement for the `config.Config` class.
    """
    _instance = None
    _buhtz = []

    @classmethod
    def instance(cls):
        """Provide the singleton instance of that class."""

       # Provide the instance if it exists
       if cls._instance:
           return cls._instance

    # But don't created implicite when needed.
    raise RuntimeError(
        f'No instance of class "{cls}" exists. Create an instance first.')

    def __init__(self):
        # Exception when an instance exists
        if __class__._instance:
            raise Exception(
                f'Instance of class "{self.__class__.__name__}" still exists! '
                f'Use "{self.__class__.__name__}.instance()" to access it.')

        # Remember the instance as the one and only singleton
        __class__._instance = self

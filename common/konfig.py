# SPDX-FileCopyrightText: © 2024 Christian BUHTZ <c.buhtz@posteo.jp>
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This file is part of the program "Back In time" which is released under GNU
# General Public License v2 (GPLv2).
# See file LICENSE or go to <https://www.gnu.org/licenses/#GPL>.
from pathlib import Path
import singleton

class Konfig(singleton.Singleton):
    """Manage configuration of Back In Time.

    That class is a replacement for the `config.Config` class.
    """
    def __init__(self, config_path: Path = None):
        """
        """
        self._determine_config_path(config_path)

    def _determine_config_path(self, path: Path):
        if path:
            self._path = path
            return

        # TODO
        # ...determine...

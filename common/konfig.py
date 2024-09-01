# SPDX-FileCopyrightText: © 2024 Christian BUHTZ <c.buhtz@posteo.jp>
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This file is part of the program "Back In Time" which is released under GNU
# General Public License v2 (GPLv2).
# See file LICENSE or go to <https://www.gnu.org/licenses/#GPL>.
from __future__ import annotations
import configparser
import getpass
import os
import socket
from typing import Union, Any, Optional
from pathlib import Path
from io import StringIO, TextIOWrapper
import singleton
import logger

# Workaround: Mostly relevant on TravisCI but not exclusively.
# While unittesting and without regular invocation of BIT the GNU gettext
# class-based API isn't setup yet.
# The bigger problem with config.py is that it do use translatable strings.
# Strings like this do not belong into a config file or its context.
try:
    _('Warning')
except NameError:
    _ = lambda val: val


class Profile:
    """Manages access to profile-specific configuration data."""
    _DEFAULT_VALUES = {
        'snapshots.mode': 'local',
        'snapshots.path.host': socket.gethostname(),
        'snapshots.path.user': getpass.getuser(),
        'snapshots.ssh.port': 22,
        'snapshots.ssh.cipher': 'default',
        'snapshots.ssh.user': getpass.getuser(),
        'snapshots.ssh.private_key_file':
            str(Path('~') / '.ssh' / 'id_rsa'),
        'snapshots.ssh.max_arg_length': 0,
        'snapshots.ssh.check_commands': True,
        'snapshots.ssh.check_ping': True,
        'snapshots.local_encfs.path': '',
        'snapshots.password.save': False,
    }

    def __init__(self, profile_id: int, config: Konfig):
        self._config = config
        self._prefix = f'profile{profile_id}'

    def __getitem__(self, key: str):
        try:
            return self._config[f'{self._prefix}.{key}']
        except KeyError:
            return self._DEFAULT_VALUES[key]

    def __setitem__(self, key: str, val: Any):
        self._config[f'{self._prefix}.{key}'] = val

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

    @snapshots_mode.setter
    def snapshots_mode(self, val: str) -> None:
        self['snapshots.mode'] = val

    @property
    def snapshots_path(self) -> str:
        """Where to save snapshots in mode 'local'. This path must contain
        a folderstructure like 'backintime/<HOST>/<USER>/<PROFILE_ID>'.

        {
            'values': 'absolute path',
        }
        """
        raise NotImplementedError(
            'see original in Config class. See also '
            'Config.snapshotsFullPath(self, profile_id = None)')

        return self['snapshots.path']

    @snapshots_path.setter
    def snapshots_path(self, path):
        raise NotImplementedError('see original in Config class.')

    @property
    def snapshots_path_host(self) -> str:
        """Set Host for snapshot path.

        { 'values': 'local hostname' }
        """
        return self['snapshots.path.host']

    @snapshots_path_host.setter
    def snapshots_path_host(self, value: str) -> None:
        self['snapshots.path.host'] = value

    @property
    def snapshots_path_user(self) -> str:
        """Set User for snapshot path.

        { 'values': 'local username' }
        """
        return self['snapshots.path.user']

    @snapshots_path_user.setter
    def snapshots_path_user(self, value: str) -> None:
        self['snapshots.path.user'] = value

    @property
    def snapshots_path_profileid(self) -> str:
        """Set Profile-ID for snapshot path

        {
            'values': '1-99999',
            'default': 'current Profile-ID'
        }
        """
        try:
            return self['snapshots.path.profile']
        except KeyError:
            # Extract number from field prefix
            # e.g. "profile1" -> "1"
            return self._prefix.replace('profile', '')

    @snapshots_path_profileid.setter
    def snapshots_path_profileid(self, value: str) -> None:
        self['snapshots.path.profile'] = value

    @property
    def ssh_snapshots_path(self) -> str:
        """Snapshot path on remote host. If the path is relative (no
        leading '/') it will start from remote Users homedir. An empty path
        will be replaced with './'.

        {
            'values': 'absolute or relative path',
        }

        """
        return self['snapshots.ssh.path']

    @ssh_snapshots_path.setter
    def ssh_snapshots_path(self, path):
        raise NotImplementedError('see original in Config class.')

    @property
    def ssh_host(self) -> str:
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
    def ssh_port(self) -> int:
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

    @property
    def ssh_user(self) -> str:
        """Remote SSH user.

        {
            'default': 'local users name',
            'values': 'text',
        }
        """
        return self['snapshots.ssh.user']

    @ssh_user.setter
    def ssh_user(self, value: str) -> None:
        self['snapshots.ssh.user'] = value

    @property
    def ssh_cipher(self) -> str:
        """Cipher that is used for encrypting the SSH tunnel. Depending on
        the environment (network bandwidth, cpu and hdd performance) a
        different cipher might be faster.

        {
            'values': 'default | aes192-cbc | aes256-cbc | aes128-ctr ' \
                        '| aes192-ctr | aes256-ctr | arcfour | arcfour256 ' \
                        '| arcfour128 | aes128-cbc | 3des-cbc | ' \
                        'blowfish-cbc | cast128-cbc',
        }
        """
        return self['snapshots.ssh.cipher']

    @ssh_cipher.setter
    def ssh_cipher(self, value: str) -> None:
        self['snapshots.ssh.cipher'] = value

    @property
    def ssh_private_key_file(self) -> Path:
        """Private key file used for password-less authentication on remote
        host.

        {
            'values': 'absolute path to private key file',
            'type': 'str'
        }

        """
        raise NotImplementedError('see original in Config class')
        path_string = self['snapshots.ssh.private_key_file']
        return Path(path_string)

    @ssh_private_key_file.setter
    def ssh_private_key_file(self, path: Path) -> None:
        self['snapshots.ssh.private_key_file'] = path

    @property
    def ssh_proxy_host(self) -> str:
        """Proxy host (or jump host) used to connect to remote host.

        {
            'values': 'IP or domain address',
        }
        """
        return self['snapshots.ssh.proxy_host']

    @ssh_proxy_host.setter
    def ssh_proxy_host(self, value: str) -> None:
        self['snapshots.ssh.proxy_host'] = value

    @property
    def ssh_proxy_port(self) -> int:
        """Port of SSH proxy (jump) host used to connect to remote host.

        {
            'values': '0-65535',
            'default': 22,
        }
        """
        return self['snapshots.ssh.proxy_port']

    @ssh_proxy_port.setter
    def ssh_proxy_port(self, value: int) -> None:
        self['snapshots.ssh.proxy_port'] = value

    @property
    def ssh_proxy_user(self) -> str:
        """SSH user at proxy (jump) host.

        {
            'default': 'local users name',
            'values': 'text',
        }
        """
        return self['snapshots.ssh.proxy_user']

    @ssh_proxy_user.setter
    def ssh_proxy_user(self, value: str) -> None:
        self['snapshots.ssh.proxy_user'] = value

    @property
    def ssh_max_arg_length(self) -> int:
        """Maximum command length of commands run on remote host. This can
        be tested for all ssh profiles in the configuration with 'python3
        /usr/share/backintime/common/sshMaxArg.py LENGTH'. The value '0'
        means unlimited length.

        {
            'values': '0, >700',
        }
        """
        raise NotImplementedError('see org in Config')
        return self['snapshots.ssh.max_arg_length']

    @ssh_max_arg_length.setter
    def ssh_max_arg_length(self, length: int) -> None:
        self['snapshots.ssh.max_arg_length'] = length

    @property
    def ssh_check_commands(self) -> bool:
        """Check if all commands (used during takeSnapshot) work like
        expected on the remote host.
        { 'values': 'true|false' }
        """
        return self['snapshots.ssh.check_commands']

    @ssh_check_commands.setter
    def ssh_check_commands(self, value: bool) -> None:
        self['snapshots.ssh.check_commands'] = value

    @property
    def ssh_check_ping_host(self) -> bool:
        """Check if the remote host is available before trying to mount.
        { 'values': 'true|false' }
        """
        return self['snapshots.ssh.check_ping']

    @ssh_check_ping_host.setter
    def ssh_check_ping_host(self, value: bool) -> None:
        self['snapshots.ssh.check_ping'] = value

    @property
    def local_encfs_path(self) -> Path:
        """Where to save snapshots in mode 'local_encfs'.

        { 'values': 'absolute path' }
        """
        return self['snapshots.local_encfs.path']

    @local_encfs_path.setter
    def local_encfs_path(self, path: Path):
        self['snapshots.local_encfs.path'] = str(path)

    @property
    def password_save(self) -> bool:
        """Save password to system keyring (gnome-keyring or kwallet).
        { 'values': 'true|false' }
        """
        raise NotImplementedError(
            'Refactor it first to make the field name mode independed. '
            'profileN.snapshots.password.save')
        return self['snapshots.password.save']

    @password_save.setter
    def password_save(self, value: bool) -> None:
        self['snapshots.password.save'] = value

    @property
    def password_use_cache(self, value: bool) -> None:
        """Cache password in RAM so it can be read by cronjobs.
        Security issue: root might be able to read that password, too.

        {
            'values': 'true|false',
            'default': 'see #1855'
        }
        """
        raise NotImplementedError(
            'Refactor it first to make the field name mode independed. '
            'profileN.snapshots.password.use_cache.'
            'See also Issue #1855 about encrypted home dir')
        # ??? default = not tools.checkHomeEncrypt()
        return self['snapshots.password.use_cache']

    @password_use_cache.setter
    def password_use_cache(self, value: bool) -> None:
        self['snapshots.password.use_cache'] = value


class Konfig(metaclass=singleton.Singleton):
    """Manage configuration data for Back In Time.

    Dev note:

        That class is a replacement for the `config.Config` class.
    """

    _DEFAULT_VALUES = {
        'global.hash_collision': 0,
        'global.language': '',
        'global.use_flock': False,
        'internal.manual_starts_countdown': 10,
    }

    _DEFAULT_SECTION = '[bit]'

    def __init__(self, buffer: Optional[TextIOWrapper, StringIO] = None):
        """Constructor.

        Args:
            buffer: An open text-file handle or a string buffer ready to read.

        Note: That method is executed only once because `Konfig` is a
        singleton.
        """
        if buffer:
            self.load(buffer)
        else:
            self._conf = {}

        # Names and IDs of profiles
        # Extract all relevant lines of format 'profile*.name=*'
        name_items = filter(
            lambda val:
                val[0].startswith('profile') and val[0].endswith('.name'),
            self._conf.items()
        )
        self._profiles = {
            name: int(pid.replace('profile', '').replace('.name', ''))
            for pid, name in name_items
        }

    def __getitem__(self, key: str) -> Any:
        try:
            return self._conf[key]
        except KeyError:
            return self._DEFAULT_VALUES[key]

    def __setitem__(self, key: str, val: Any) -> None:
        self._conf[key] = val

    def profile(self, name_or_id: Union[str, int]) -> Profile:
        """Return a `Profile` object related to the given name or id.

        Args:
            name_or_id: A name or an numeric id of a snapshot profile.

        Raises:
            KeyError: If no corresponding profile exists.
        """
        if isinstance(name_or_id, int):
            profile_id = name_or_id
        else:
            profile_id = self._profiles[name_or_id]

        return Profile(profile_id=profile_id, config=self)

    @property
    def profile_names(self) -> list[str]:
        return list(self._profiles.keys())

    @property
    def profile_ids(self) -> list[int]:
        return list(self._profiles.values())

    def load(self, buffer: Union[TextIOWrapper, StringIO]):
        """Load configuration from file like object.

        Args:
            buffer: An open text-file handle or a string buffer ready to read.
        """

        self._config_parser = configparser.ConfigParser(
            interpolation=None,
            defaults={'profile1.name': _('Main profile')})

        # raw content
        content = buffer.read()

        # Add section header to make it a real INI file
        self._config_parser.read_string(f'{self._DEFAULT_SECTION}\n{content}')

        # The one and only main section
        self._conf = self._config_parser[self._DEFAULT_SECTION[1:-1]]

    def save(self, buffer: TextIOWrapper):
        """Store configuraton to the config file."""

        raise NotImplementedError('Prevent overwritting real config data.')

        tmp_io_buffer = StringIO()
        self._config_parser.write(tmp_io_buffer)
        tmp_io_buffer.seek(0)

        # Write to file without section header
        # Discard unwanted first line
        tmp_io_buffer.readline()
        handle.write(tmp_io_buffer.read())

    @property
    def hash_collision(self) -> int:
        """Internal value used to prevent hash collisions on mountpoints.
        Do not change this.

        {
            'values': '0-99999',
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

    @property
    def manual_starts_countdown(self) -> int:
        # Countdown value about how often the users started the Back In Time
        # GUI.

        # It is an internal variable not meant to be used or manipulated be the
        # users. At the end of the countown the
        # :py:class:`ApproachTranslatorDialog` is presented to the user.
        return self['internal.manual_starts_countdown']

    def decrement_manual_starts_countdown(self):
        """Counts down to -1.

        See `manual_starts_countdown()` for details.
        """
        val = self.manual_starts_countdown

        if val > -1:
            self['internal.manual_starts_countdown'] = val - 1


def config_file_path() -> Path:
    """Return the config file path.

    Could be moved into backintime.py. sys.argv (--config) needs to be
    considered.
    """
    xdg_config = os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config')
    path = Path(xdg_config) / 'backintime' / 'config'

    logger.debug(f'Config path: {path}')

    return path


if __name__ == '__main__':
    # Empty in-memory config file
    # k = Konfig(StringIO())

    x = Konfig()
    print(x)
    print(x._conf)

    # Regular config file
    with config_file_path().open('r', encoding='utf-8') as handle:
        k = Konfig()
        k.load(handle)

    print(k)
    print(k._conf)

    print(f'{k.profile_names=}')
    print(f'{k.profile_ids=}')
    print(f'{k.hash_collision=}')
    print(f'{k.language=}')
    print(f'{k.global_flock=}')

    p = k.profile(2)
    print(f'{p.snapshots_mode=}')
    p.snapshots_mode='ssh'
    print(f'{p.snapshots_mode=}')

    k.foobarasd = 7
    p.foobarasd = 7

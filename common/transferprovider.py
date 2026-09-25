# SPDX-FileCopyrightText: © 2026 Christian Buhtz <c.buhtz@posteo.jp>
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This file is part of the program "Back In Time" which is released under GNU
# General Public License v2 (GPLv2). See LICENSES directory or go to
# <https://spdx.org/licenses/GPL-2.0-or-later.html>.
"""Provide paths and temporary mounts required for rsync and similar
operations.

The paths used for an rsync transfer are not necessarily identical to
the paths used for normal filesystem operations. The TransferProvider
provides suitable source and destination paths for an individual
transfer and manages any temporary mounts required for that
representation. Temporary mounts are created for the duration of
the transfer and removed afterwards.

The four profile variants are handled as follows:

* local
    The backup storage is directly accessible as a local path.
    No additional mount is required.

    Source:      /home/eva/Source
    Destination: /home/eva/Destination

* ssh
    The actual remote backup path is used as the remote endpoint.

    Source:      /home/eva/Source
    Destination: walle@earth:/home/walle/Destination

* local + gocryptfs
    A temporary reverse gocryptfs mount is used to provide an
    encrypted view of the source directory. Rsync then works directly
    with the encrypted representation of source and destination.

    Source:      /home/eva/.local/share/backintime/mnt/B2DF6A2D
                 (mountpoint for /home/eva/Source)
    Destination: /home/eva/Destination

* ssh + gocryptfs
    Similar to 'local + gocryptfs', a temporary reverse gocryptfs view
    is used as the local rsync source and the actual remote backup path
    is used as the rsync destination.

    Source:      /home/eva/.local/share/backintime/mnt/B2DF6A2D
                 (mountpoint for /home/eva/Source)
    Destination: walle@earth:/home/walle/Destination

Using a reverse gocryptfs view for encrypted transfers keeps rsync
working on the encrypted representation of the backup. In particular,
for SSH profiles this allows rsync to use the normal remote-transfer
mechanism instead of treating an SSHFS mount as a local destination.
This also allows rsync to perform its normal remote-side operations on
the encrypted backup data.

The TransferProvider is deliberately separate from the MountManager.
The MountManager provides the persistent working representation of the
backup storage for Back In Time's filesystem operations. The
TransferProvider provides the representation required for a particular
data transfer, including the actual remote rsync endpoint and any
temporary transfer mounts.

The TransferProvider must not assume that the path used by the
MountManager is also a valid rsync source or destination.
"""
from pathlib import Path
import logger
from mount import MountManager


class TransferProvider:
    """Provide paths and temporary mounts required for rsync and similar
    operations.
    """
    def __init__(self, mount_manager: MountManager, source, destination):
        logger.debug(f'Init {__class__} : {source=} {destination=}')

        self._mount_manager = mount_manager
        self._source = source
        self._destination = destination

        self._transfer_source = None
        self._transfer_destination = None

    def __enter__(self):
        # Prepare transfer, including temporary mounts.

        if self._mount_manager.uses_ssh:
            raise NotImplementedError

        if self._mount_manager.uses_encryption:
            raise NotImplementedError

        # Local
        self._transfer_source = self._source
        self._transfer_destination = self._destination

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Cleanp temporary mounts.
        pass

    def source(self):
        """Return the source path for the transfer."""
        return self._transfer_source

    def destination(self):
        """Return the destination path for the transfer."""
        return self._transfer_destination

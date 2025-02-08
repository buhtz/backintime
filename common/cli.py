# SPDX-FileCopyrightText: © 2008-2022 Germar Reitze
# SPDX-FileCopyrightText: © 2024 Christian Buhtz <c.buhtz@posteo.jp>
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This file is part of the program "Back In Time" which is released under GNU
# General Public License v2 (GPLv2). See file/folder LICENSE or go to
# <https://spdx.org/licenses/GPL-2.0-or-later.html>.
import os
import sys
import tools
import daemon
import snapshots
import bcolors

def restore(cfg, snapshot_id = None, what = None, where = None, **kwargs):
    if what is None:
        what = input('File to restore: ')
    what = tools.preparePath(os.path.abspath(os.path.expanduser(what)))

    if where is None:
        where = input('Restore to (empty for original path): ')
    if where:
        where = tools.preparePath(os.path.abspath(os.path.expanduser(where)))

    snapshotsList = snapshots.listSnapshots(cfg)

    sid = selectSnapshot(snapshotsList, cfg, snapshot_id, 'SnapshotID to restore')
    print('')
    RestoreDialog(cfg, sid, what, where, **kwargs).run()

def remove(cfg, snapshot_ids = None, force = None):
    snapshotsList = snapshots.listSnapshots(cfg)
    if not snapshot_ids:
        snapshot_ids = (None,)
    sids = [selectSnapshot(snapshotsList, cfg, sid, 'SnapshotID to remove') for sid in snapshot_ids]

    if not force:
        print('Do you really want to remove these snapshots?')
        [print(sid.displayName) for sid in sids]
        if not 'yes' == input('(no/yes): '):
            return

    s = snapshots.Snapshots(cfg)
    [s.remove(sid) for sid in sids]

def checkConfig(cfg, crontab = True):
    import mount
    from exceptions import MountException

    def announceTest():
        print()
        print(frame(test))

    def failed():
        print(test + ': ' + bcolors.FAIL + 'failed' + bcolors.ENDC)

    def okay():
        print(test + ': ' + bcolors.OKGREEN + 'done' + bcolors.ENDC)

    def errorHandler(msg):
        print(bcolors.WARNING + 'WARNING: ' + bcolors.ENDC + msg)

    cfg.setErrorHandler(errorHandler)
    mode = cfg.snapshotsMode()

    if cfg.SNAPSHOT_MODES[mode][0] is not None:
        #preMountCheck
        test = 'Run mount tests'
        announceTest()
        mnt = mount.Mount(cfg = cfg, tmp_mount = True)

        try:
            mnt.preMountCheck(mode = mode, first_run = True)

        except MountException as ex:
            failed()
            print(str(ex))
            return False

        okay()

        #okay, lets try to mount
        test = 'Mount'
        announceTest()

        try:
            hash_id = mnt.mount(mode=mode, check=False)

        except MountException as ex:
            failed()
            print(str(ex))
            return False

        okay()

    test = 'Check/prepare snapshot path'
    announceTest()
    snapshots_mountpoint = cfg.get_snapshots_mountpoint(tmp_mount=True)

    ret = tools.validate_and_prepare_snapshots_path(
        path=snapshots_mountpoint,
        host_user_profile=cfg.hostUserProfile(),
        mode=mode,
        copy_links=cfg.copyLinks(),
        error_handler=cfg.notifyError)

    if not ret:
        failed()
        return False

    okay()

    # umount
    if not cfg.SNAPSHOT_MODES[mode][0] is None:
        test = 'Unmount'
        announceTest()

        try:
            mnt.umount(hash_id=hash_id)

        except MountException as ex:
            failed()
            print(str(ex))
            return False

        okay()

    test = 'Check config'
    announceTest()

    if not cfg.checkConfig():
        failed()
        return False

    okay()

    if crontab:
        test = 'Install crontab'
        announceTest()

        if not cfg.setupCron():
            failed()
            return False

        okay()

    return True

def selectSnapshot(snapshotsList, cfg, snapshot_id = None, msg = 'SnapshotID'):
    """
    check if given snapshot is valid. If not print a list of all
    snapshots and ask to choose one
    """
    len_snapshots = len(snapshotsList)

    if not snapshot_id is None:
        try:
            sid = snapshots.SID(snapshot_id, cfg)
            if sid in snapshotsList:
                return sid
            else:
                print('SnapshotID %s not found.' % snapshot_id)
        except ValueError:
            try:
                index = int(snapshot_id)
                return snapshotsList[index]
            except (ValueError, IndexError):
                print('Invalid SnaphotID index: %s' % snapshot_id)
    snapshot_id = None

    columns = (terminalSize()[1] - 25) // 26 + 1
    rows = len_snapshots // columns
    if len_snapshots % columns > 0:
        rows += 1

    print('SnapshotID\'s:')
    for row in range(rows):
        line = []
        for column in range(columns):
            index = row + column * rows
            if index > len_snapshots - 1:
                continue
            line.append('{i:>4}: {s}'.format(i = index, s = snapshotsList[index]))
        print(' '.join(line))
    print('')
    while snapshot_id is None:
        try:
            index = int(input(msg + ' (0 - %d): ' % (len_snapshots - 1)))
            snapshot_id = snapshotsList[index]
        except (ValueError, IndexError):
            print('Invalid Input')
            continue
    return snapshot_id

def terminalSize():
    """
    get terminal size
    """
    for fd in (sys.stdin, sys.stdout, sys.stderr):
        try:
            import fcntl
            import termios
            import struct
            return [int(x) for x in struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))]
        except ImportError:
            pass
    return [24, 80]

def frame(msg, size = 32):
    ret  = ' +' + '-' * size +       '+\n'
    ret += ' |' + msg.center(size) + '|\n'
    ret += ' +' + '-' * size +       '+'
    return ret

class RestoreDialog:
    def __init__(self, cfg, sid, what, where, **kwargs):
        self.config = cfg
        self.sid = sid
        self.what = what
        self.where = where
        self.kwargs = kwargs

        self.logFile = self.config.restoreLogFile()
        if os.path.exists(self.logFile):
            os.remove(self.logFile)

    def callback(self, line, *params):
        if not line:
            return
        print(line)
        with open(self.logFile, 'a') as log:
            log.write(line + '\n')

    def run(self):
        s = snapshots.Snapshots(self.config)
        s.restore(self.sid, self.what, self.callback, self.where, **self.kwargs)
        print('\nLog saved to %s' % self.logFile)

class BackupJobDaemon(daemon.Daemon):
    def __init__(self, func, args):
        super(BackupJobDaemon, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.func(self.args, False)

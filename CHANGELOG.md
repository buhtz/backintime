# Changelog
[![Common Changelog](https://common-changelog.org/badge.svg)](https://common-changelog.org)
<!-- Template
## Unreleased
### Changed
### Added
### Removed
### Fixed
-->

## 1.4.4-dev (development of upcoming release)

### Fixed

- Validation of diff command settings in compare snapshots dialog (#1662) (@stcksmsh Kosta Vukicevic)
- Open symlinked folders in file view (#1476)
- Respect dark mode using color roles (#1601)
- "Highly recommended" exclusion pattern in "Manage Profile" dialog's "Exclude" tab show missings only (#1620)
- `make install` ignored $(DEST) in file migration part (#1630)

### Uncategorized

- Build : Activate PyLint error E0401 (import-error)
- Dependency : Migration to PyQt6
- Build : PyLint unit test is skipped if PyLint isn't installed, but will always run on TravisCI (#1634)
- Build : Git commit hash is presevered while "make install" (#1637)
- Build : Fix bash-completion symlink creation while installing & adding --diagnostics (#1615)
- Build : Activate PyLint error E602 (undefined-variable)
- Build : TravisCI use PyQt (except arch "ppc64le")

### Added

- Support rsync '--one-file-system' in Expert Options (#1598)
- "*-dev" version strings contain last commit hash (#1637)

## 1.4.3 (2024-01-30)

### Added

- Exclude 'SingletonLock' and 'SingletonCookie' (Discord) and 'lock' (Mozilla Firefox) files by default (part of #1555)

### Uncategorized

- Work around : Relax `rsync` exit code 23: Ignore instead of error now (part of #1587)
- Feature (experimental) : Add new snapshot log filter `rsync transfer failures (experimental)` to find them easier (they are normally not shown as "error").  
- Improve : Launcher for BiT GUI (root) does not enforce Wayland anymore but uses same settings as for BiT GUI (userland) (#1350)
- Change of semantics : BiT running as root never disables suspend during taking a backup ("inhibit suspend") even though this may have worked before in BiT <= v1.4.1 sometimes (required to fix #1592)
- Build : Use PyLint in unit testing to catch E1101 (no-member) errors.
- Build : Activate PyLint warning W1401 (anomalous-backslash-in-string).
- Build : Add codespell config.
- Build : Allow manual specification of python executable (--python=PYTHON_PATH) in common/configure and qt/configure
- Build : All starter scripts do use an absolute path to the python executable by default now via common/configure and qt/configure (#1574)
- Build : Install dbus configuration file to /usr/share not /etc (#1596)
- Build : `configure` does delete old installed files (`qt4plugin.py` and `net.launchpad.backintime.serviceHelper.conf`) that were renamed or moved in a previous release (#1596)
- Translation : Minor modifications in source strings and updating language files.
- Refactor : Solved circular dependency between tools.py and logger.py to fix #820
- Improved : qtsystrayicon.py, qt5_probing.py, usercallbackplugin.py and all parts of app.py 

### Fixed

- 'qt5_probing.py' hangs when BiT is run as root and no user is logged into a desktop environment (#1592 and #1580)
- Launching BiT GUI (root) hangs on Wayland without showing the GUI (#836)
- Disabling suspend during taking a backup ("inhibit suspend") hangs when BiT is run as root and no user is logged into a desktop environment (#1592)
- RTE: module 'qttools' has no attribute 'initate_translator' with encFS when prompting the user for a password (#1553).
- Schedule dropdown menu used "minutes" instead of "hours".
- Unhandled exception "TypeError: 'NoneType' object is not callable" in tools.py function __log_keyring_warning (#820). 

## 1.4.1 (2023-10-01)

### Uncategorized

- Dependency : Add "qt translations" to GUI runtime dependencies (#1538).
- Build : Unit tests do generically ignore all instead of well-known warnings now (#1539).
- Build : Warnings about missing Qt translation now are ignored while testing (#1537).

### Fixed

- GUI didn't start when "show hidden files" button was on (#1535).

## 1.4.0 (2023-09-14)

### Uncategorized

- Project : Renamed branch "master" to "main" and started "gitflow" branching model.
- Refactor : Renamed qt4plugin.py to systrayiconplugin.py (we are using Qt5 for years now ;-)
- Refactor : Removed unfinished feature "Full system backup" (#1526)
- GUI Change : View last (snapshot) log button in GUI uses "document-open-recent" icon now instead of "document-new" (#1386)
- Breaking change : Minimal Python version 3.8 required (#1358).
- Removed : Handling and checking of user group "fuse" (#1472).
- Documentation : Removed outdated docbook (#1345).
- Build : Introduced .readthedocs.yaml as asked by ReadTheDocs.org (#1443).
- Dependency : The oxygen icons should be installed with the BiT Qt GUI since they are used as fallback in case of missing icons
- Translation : Strings to translate now easier to understand for translators (#1448, #1457, #1462, #1465).
- Translation : Improved completeness of translations and additional modifications of source strings (#1454, #1512)
- Translation : Plural forms support (#1488).
- Removed : Translation in Canadian English, British English and Javanese (#1455).
- Added : Translation in Persian and Vietnamese (#1460).
- Added : Message to users (after 10 starts of BIT Gui) to motivate them contributing translations (#1473).

### Fixed

- AttributeError: can't set attribute 'showHiddenFiles' in app.py (#1532)
- Check SSH login works on machines with limited commands (#1442)
- Missing icon in SSH private key button (#1364)
- Master issue for missing or empty system-tray icon (#1306)
- System-tray icon missing or empty (GUI and cron) (#1236)
- Improve KDE plasma icon compatibility (#1159)
- Unit test fails on some machines due to warning "Ignoring XDG_SESSION_TYPE=wayland on Gnome..." (#1429)
- Generation of config-manpage caused an error with Debian's Lintian (#1398).
- Return empty list in smartRemove (#1392, Debian Bug Report 973760)
- Taking a snapshot reports `rsync` errors now even if no snapshot was taken (#1491)
- takeSnapshot() recognizes errors now by also evaluating the rsync exit code (#489) 
- The error user-callback is now always called if an error happened while taking a snapshot (#1491)
- D-Bus serviceHelper error "LimitExceeded: Maximum length of command line reached (100)": 
- Treat rsync exit code 24 as INFO instead of ERROR (#1506)
- Add support for ChainerBackend class as keyring which iterates over all supported keyring backends (#1410)

### Added

- Introduce new error codes for the "error" user callback (as part of #1491):  
- The `rsync` exit code is now contained in the snapshot log (part of #489). Example: 
- Exclude /swapfile by default (#1053)
- Rearranged menu bar and its entries in the main window (#1487, #1478).
- Configure user interface language via config file and GUI.

## 1.3.3 (2023-01-04)

### Added

- New command line argument "--diagnostics" to show helpful info for better issue support (#1100)
- Write all log output to stderr; do not pollute stdout with INFO and WARNING messages anymore (#1337)

### Uncategorized

- GUI change : Remove Exit button from the toolbar (#172)
- GUI change : Define accelerator keys for menu bar and tabs, as well as toolbar shortcuts (#1104)
- Desktop integration : Update .desktop file to mark Back In Time as a single main window program (#1258)
- Documentation update : Correct description of profile<N>.schedule.time in backintime-config manpage (#1270)
- Translation update : Brazilian Portuguese (#1267)
- Translation update : Italian (#1110, #1123)
- Translation update : French (#1077)
- Testing : Fix a test fail when dealing with an empty crontab (#1181)
- Testing : Fix a test fail when dealing with an empty config file (#1305)
- Testing : Skip "test_quiet_mode" (does not work reliably)
- Testing : Improve "test_diagnostics_arg" (introduced with #1100) to no longer fail 
- Testing : Numerous fixes and extensions to testing (#1115, #1213, #1279, #1280, #1281, #1285, #1288, #1290, #1293, #1309, #1334)

### Fixed

- RTE "reentrant call inside io.BufferedWriter" in logFile.flush() during backup (#1003)
- Incompatibility with rsync 3.2.4 or later because of rsync's "new argument protection" (#1247). Deactivate "--old-args" rsync argument earlier recommended to users as a workaround.
- DeprecationWarnings about invalid escape sequences.
- AttributeError in "Diff Options" dialog (#898)
- Settings GUI: "Save password to Keyring" was disabled due to "no appropriate keyring found" (#1321)
- Back in Time did not start with D-Bus error   
- Avoid logging errors while waiting for a target drive to be mounted (#1142, #1143, #1328)
- [Arch Linux] AUR pkg "backintime-git": Build tests fails and installation is aborted (#1233, fixed with #921)
- Wrong systray icon showing in Wayland (#1244)

## 1.3.2 (2022-03-12)

### Fixed

- Tests no longer work with Python 3.10 (https://github.com/bit-team/backintime/issues/1175)

## 1.3.1 (2021-07-05)

### Uncategorized

- Uncategorized : bump version, forgot to push branch to Github before releasing

## 1.3.0 (2021-07-04)

### Uncategorized

- Merge PR : Fix FileNotFoundError exception in mount.mounted, Thanks tatokis (https://github.com/bit-team/backintime/pull/1157)
- Merge PR : qt/plugins/notifyplugin: Fix setting self.user, not local variable, Thanks Zocker1999NET (https://github.com/bit-team/backintime/pull/1155)
- Merge PR : Use Link Color instead of lightGray as not to break theming, Thanks newhinton (https://github.com/bit-team/backintime/pull/1153)
- Merge PR : Match old and new rsync version format, Thanks TheTimeWalker (https://github.com/bit-team/backintime/pull/1139)
- Merge PR : 'TempPasswordThread' object has no attribute 'isAlive', Thanks FMeinicke (https://github.com/bit-team/backintime/pull/1135)
- Merge PR : Keep permissions of an existing mountpoint from being overridden, Thanks bentolor (https://github.com/bit-team/backintime/pull/1058)

### Fixed

- YEAR missing in config (https://github.com/bit-team/backintime/issues/1023)
- SSH module didn't send identification string while checking if remote host is available (https://github.com/bit-team/backintime/issues/1030)

## 1.2.1 (2019-08-25)

### Fixed

- TypeError in backintime.py if mount failed while running a snapshot (https://github.com/bit-team/backintime/issues/1005)

## 1.2.0 (2019-04-27)

### Fixed

- Exit code is linked to the wrong status message (https://github.com/bit-team/backintime/issues/906)
- AppName showed 'python3' instead of 'Back In Time' (https://github.com/bit-team/backintime/issues/950)
- configured cipher is not used with all ssh-commands (https://github.com/bit-team/backintime/issues/934)
- 'make test' fails because local SSH server is running on non-standard port (https://github.com/bit-team/backintime/issues/945)
- 23:00 is missing in the list of every day hours (https://github.com/bit-team/backintime/issues/736)
- ssh-agent output changed (https://github.com/bit-team/backintime/issues/840)
- exception on making backintime folder world writable (https://github.com/bit-team/backintime/issues/812)
- stat free space for snapshot folder instead of backintime folder (https://github.com/bit-team/backintime/issues/733)
- backintime root crontab doesn't run; missing line-feed 0x0A on last line (https://github.com/bit-team/backintime/issues/781)
- IndexError in inhibitSuspend (https://github.com/bit-team/backintime/issues/772)
- polkit CheckAuthorization: race condition in privilege authorization (https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-7572)
- OSError when running backup-job from systemd (https://github.com/bit-team/backintime/issues/720)
- restore filesystem-root without 'Full rsync mode' with ACL and/or xargs activated broke whole system (https://github.com/bit-team/backintime/issues/708)
- use current folder if no file is selected in files view (https://github.com/bit-team/backintime/issues/687, https://github.com/bit-team/backintime/issues/685)
- don't reload profile after editing profile name (https://github.com/bit-team/backintime/issues/706)
- Exception in FileInfo
- failed to restore suid permissions (https://github.com/bit-team/backintime/issues/661)
- on remount user-callback got called AFTER trying to mount (https://github.com/bit-team/backintime/issues/654)
- confirm restore dialog has no scroll bar (https://github.com/bit-team/backintime/issues/625)
- DEFAULT_EXCLUDE not deletable (https://github.com/bit-team/backintime/issues/634)
- GUI status bar unreadable (https://github.com/bit-team/backintime/issues/612)
- udev schedule not working (https://github.com/bit-team/backintime/issues/605)
- decode path spooled from /etc/mtab (https://github.com/bit-team/backintime/pull/607)
- in snapshots.py, gives more helpful advice if a lock file is present that shouldn't be.  (https://github.com/bit-team/backintime/issues/601)
- Fail to create remote snapshot path with spaces (https://github.com/bit-team/backintime/issues/567)
- broken new_snapshot can run into infinite saveToContinue loop (https://github.com/bit-team/backintime/issues/583)
- udev schedule didn't work with LUKS encrypted drives (https://github.com/bit-team/backintime/issues/466)
- sshMaxArg failed on none default ssh port (https://github.com/bit-team/backintime/issues/581)
- failed if remote host send SSH banner (https://github.com/bit-team/backintime/issues/581)
- incorrect handling of IPv6 addresses (https://github.com/bit-team/backintime/issues/577)
- Snapshot Log View freeze on big log files (https://github.com/bit-team/backintime/issues/456)
- 'inotify_add_watch failed: file or directory not found' after deleting snapshot
- a continued snapshot was not incremental (https://github.com/bit-team/backintime/issues/557)
- config backup in snapshot had wrong name if using --config option
- Can't open files with spaces in name (https://github.com/bit-team/backintime/issues/552)
- BIT-root won't start from .desktop file (https://github.com/bit-team/backintime/issues/549)
- Keyring doesn't work with KDE Plasma5 (https://github.com/bit-team/backintime/issues/545)
- Qt4 built-in phrases where not translated (https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=816197)
- configure ignore unknown args (https://github.com/bit-team/backintime/issues/547)
- snapshots-list on command-line was not sorted
- SHA256 ssh-key fingerprint was not detected
- new snapshot did not show up after finished
- TimeLine headers were not correct
- wildcards ? and [] wasn't recognized correctly
- last char of last element in tools.get_rsync_caps got cut off
- TypeError in tools.get_git_ref_hash
- don't include empty values in list (https://github.com/bit-team/backintime/issues/521)
- bash-completion doesn't work for backintime-qt4
- 'make unittest' incorrectly used 'coverage' by default (https://github.com/bit-team/backintime/issues/522)
- pm-utils is deprecated; Remove dependency (https://github.com/bit-team/backintime/issues/519)

### Uncategorized

- minor changes to allow running BiT inside Docker (https : //github.com/bit-team/backintime/pull/959)
- remove progressbar on systray icon until BiT has it's own icon (https : //github.com/bit-team/backintime/issues/902)
- clarify 'nocache' option (https : //github.com/bit-team/backintime/issues/857)
- create a config-backup in root dir if backup is encrypted (https : //github.com/bit-team/backintime/issues/556)
- Uncategorized : remove unused and undocumented userscript plugin
- Uncategorized : add contextmenu for logview dialog which can copy, exclude and decode lines
- Uncategorized : move progressbar under statusbar
- alleviate default exclude [Tt]rash* (https : //github.com/bit-team/backintime/issues/759)
- enable high DPI scaling (https : //github.com/bit-team/backintime/issues/732)
- Smart Remove try to keep healthy snapshots (https : //github.com/bit-team/backintime/issues/703)
- ask for restore-to path before confirm (https : //github.com/bit-team/backintime/issues/678)
- fix 'Back in Time (root)' on wayland (https : //github.com/bit-team/backintime/issues/640)
- sort int values in config numerical instead if alphabetical (https : //github.com/bit-team/backintime/issues/175#issuecomment-272941811)
- set timestamp directly after new snapshot (https : //github.com/bit-team/backintime/issues/584)
- add shortcut CTRL+H for toggle show hidden files to fileselect dialog (https : //github.com/bit-team/backintime/issues/378)
- Uncategorized : add 'Edit user-callback' dialog
- redesign restore menu (https : //github.com/bit-team/backintime/issues/661)
- add ability to disable SSH command- and ping-check (https : //github.com/bit-team/backintime/issues/647)
- enable bwlimit for local profiles (https : //github.com/bit-team/backintime/issues/646)
- Uncategorized : import remote host-key into known_hosts from Settings
- Uncategorized : copy public SSH key to remote host from Settings
- Uncategorized : create a new SSH key from Settings
- Uncategorized : rename debian package from backintime-qt4 into backintime-qt
- Uncategorized : rename paths and methods from *qt4* into *qt*
- Uncategorized : rename executable backintime-qt4 into backintime-qt
- Uncategorized : new config version 6, rename qt4 keys into qt, add new domain for schedule
- check crontab entries on every GUI startup (https : //github.com/bit-team/backintime/issues/129)
- Uncategorized : start a new ssh-agent instance only if necessary
- add cli command 'shutdown' (https : //github.com/bit-team/backintime/issues/596)
- Uncategorized : add cli command 'smart-remove'
- make LogView and Settings Dialog non-modal (https : //github.com/bit-team/backintime/issues/608)
- port to Qt5/pyqt5 (https : //github.com/bit-team/backintime/issues/518)
- Uncategorized : Recognize changes on previous runs while continuing new snapshots
- Add pause, resume and stop function for running snapshots (https : //github.com/bit-team/backintime/issues/474, https://github.com/bit-team/backintime/issues/195)
- Uncategorized : use rsync to save permissions
- Uncategorized : replace os.system calls with subprocess.Popen
- Uncategorized : automatically refresh log view if a snapshot is currently running
- Uncategorized : remove dependency for extended 'find' command on remote host
- Uncategorized : make full-rsync mode default, remove the other mode
- use rsync to remove snapshots which will give a nice speedup (https : //github.com/bit-team/backintime/issues/151)
- Uncategorized : open temporary local copy of files instead of original backup on double-click in GUI
- Uncategorized : add option to decrypt paths in systray menu with mode ssh-encrypted
- Uncategorized : open current log directly from systray icon during taking a snapshot
- Uncategorized : add tool-tips to restore menu
- Uncategorized : add --share-path option
- Uncategorized : use Monospace font in logview
- Uncategorized : add restore option --only-new
- Uncategorized : add button 'Take snapshot with checksums'
- Uncategorized : change default configure option to --no-fuse-group as Ubuntu >= 12.04 don't need fuse group-membership anymore
- Fix lintian warning : manpage-has-errors-from-man: bad argument name 'P'
- Uncategorized : Do not print 'SnapshotID' or 'SnapshotPath' if running 'snapshots-list' command (and other) with '--quiet'
- Uncategorized : Remove dependency 'ps'
- Uncategorized : rewrite huge parts of snapshots.py
- Uncategorized : remove backwards compatibility to version < 1.0

## 1.1.24 (2017-11-07)

### Fixed

- CVE-2017-16667: shell injection in notify-send (https://github.com/bit-team/backintime/issues/834)

## 1.1.22 (2017-10-28)

### Fixed

- stat free space for snapshot folder instead of backintime folder (https://github.com/bit-team/backintime/issues/552733)
- backintime root crontab doesn't run; missing line-feed 0x0A on last line (https://github.com/bit-team/backintime/issues/552781)
- can't open files with spaces in name (https://github.com/bit-team/backintime/issues/552552)

## 1.1.20 (2017-04-09)

### Fixed

- CVE-2017-7572: polkit CheckAuthorization: race condition in privilege authorization

## 1.1.18 (2017-03-29)

### Fixed

- manual snapshots from GUI didn't work (https://github.com/bit-team/backintime/issues/728)

## 1.1.16 (2017-03-28)

### Fixed

- start a new ssh-agent instance only if necessary (https://github.com/bit-team/backintime/issues/722)
- OSError when running backup-job from systemd (https://github.com/bit-team/backintime/issues/720)

## 1.1.14 (2017-03-05)

### Fixed

- udev schedule not working (https://github.com/bit-team/backintime/issues/605)
- Keyring doesn't work with KDE Plasma5 (https://github.com/bit-team/backintime/issues/545)
- nameError in tools.make_dirs (https://github.com/bit-team/backintime/issues/622)
- use current folder if no file is selected in files view
- restore filesystem-root without 'Full rsync mode' with ACL and/or xargs activated broke whole system (https://github.com/bit-team/backintime/issues/708)

## 1.1.12 (2016-01-11)

### Fixed

- remove x-terminal-emulator dependency (https://github.com/bit-team/backintime/issues/515)
- AttributeError in About Dialog (https://github.com/bit-team/backintime/issues/515)

## 1.1.10 (2016-01-09)

### Fixed

- failed to remove empty lock file (https://github.com/bit-team/backintime/issues/505)
- Restore the correct file owner and group fail if they are not present in system (https://github.com/bit-team/backintime/issues/58)
- QObject::startTimer error on closing app
- FileNotFoundError while starting pw-cache from source
- suppress warning about failed inhibit suspend if run as root (https://github.com/bit-team/backintime/issues/500)
- UI blocked/grayed out while removing snapshot (https://github.com/bit-team/backintime/issues/487)
- pw-cache failed on leftover PID file, using ApplicationInstance now (https://github.com/bit-team/backintime/issues/468)
- failed to parse some arguments (https://github.com/bit-team/backintime/issues/492)
- failed to start GUI if launched from systray icon
- deleted snapshot is still listed in Timeline if using mode SSH (https://github.com/bit-team/backintime/issues/493)
- PermissionError while deleting readonly files on sshfs mounted share (https://github.com/bit-team/backintime/issues/490)
- create new encrypted profiles with encfs >= 1.8.0 failed (https://github.com/bit-team/backintime/issues/477)
- AttributeError in common/tools.py if keyring is missing (https://github.com/bit-team/backintime/issues/473)
- remote rename of 'new_snapshot' folder sometimes isn't recognized locally; rename local now (https://answers.launchpad.net/questions/271792)

### Uncategorized

- Add Icon 'show-hidden' (https : //github.com/bit-team/backintime/issues/507)
- Uncategorized : Add Modify for Full System Backup button to settings page, to change some profile settings
- Uncategorized : add get|set_list_value to configfile
- Uncategorized : subclass ApplicationInstance in GUIApplicationInstance to reduce redundant code
- Uncategorized : speed up app start by adding snapshots to timeline in background thread
- add warning on failed permission restore (https : //github.com/bit-team/backintime/issues/58)
- Uncategorized : add unittest (thanks to Dorian, Alexandre, Aurélien and Gregory from IAGL)
- continue an unfinished new_snapshot if possible (https : //github.com/bit-team/backintime/issues/400)
- Add Nautilus-like shortcuts for navigating in file browser (https : //github.com/bit-team/backintime/issues/483)
- Uncategorized : speed up mounting of SSH+encrypted profiles
- Uncategorized : Move source code and bug tracking to GitHub

## 1.1.8 (2015-09-28)

### Fixed

- unlock private SSH key run into 5sec timeout if password is empty
- BiT freeze when activate 'Decode path' in 'Snapshot Log View'
- empty gray window appears when starting the gui as root (https://launchpad.net/bugs/1493020)
- gnu_find_suffix_support doesn't set back to True (https://launchpad.net/bugs/1487781)
- dbus exception if dbus systembus is not running
- depend on virtual package cron-daemon instead of cron for compatibility with other cron implementations (https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=776856)
- wasn't able to start from alternate install dir (https://launchpad.net/bugs/478689)
- wasn't able to start from source dir
- 'Inhibit Suspend' fails with 'org.freedesktop.PowerManagement.Inhibit' (https://launchpad.net/bugs/1485242)
- No mounting while selecting a secondary profile in the gui (https://launchpad.net/bugs/1481267)
- fix for bug #1419466 broke crontab on Slackware (https://launchpad.net/bugs/1478576)
- fix for bug #1431305 broke pw-cache on Ubuntu (https://launchpad.net/bugs/1431305)
- Settings accepted empty strings for Host/User/Profile-ID (https://launchpad.net/bugs/1477733)
- IndexError on 'check_remote_commands' due to too long args (https://launchpad.net/bugs/1471930)
- Makefile has no uninstall target (https://launchpad.net/bugs/1469152)

### Uncategorized

- show current app name and profile ID in syslog (https : //launchpad.net/bugs/906213)
- Show 'Profiles' dropdown only in 'Last Log Viewer', add 'Snapshots' dropdown in 'Snapshot Log Viewer' (https : //launchpad.net/bugs/1478219)
- Uncategorized : do not restore permission if they are identical with current permissions
- security issue : do not run user-callback in a shell
- Uncategorized : add option to not log user-callback output
- Uncategorized : Fix lintian warning dbus-policy-without-send-destination
- Uncategorized : apply timestamps-in-gzip.patch from Debian backintime/1.1.6-1 package
- run multiple smart-remove jobs in one screen session (https : //launchpad.net/bugs/1487781)
- Uncategorized : add error messages if PID file creation fail
- Uncategorized : Add Warning about unsupported filesystems
- Uncategorized : use native Python code to check mountpoint
- Add expert option for stdout and stderr redirection in cronjobs (https : //answers.launchpad.net/questions/270105)
- Uncategorized : remove shebang in common/askpass.py and common/create-manpage-backintime-config.py
- Uncategorized : Fix bash-complete
- show 'man backintime' on Help; remove link to backintime.le-web.org (https : //launchpad.net/bugs/1475995)
- Uncategorized : add --debug argument
- add --local-backup, --no-local-backup and --delete option to restore on command-line (https : //launchpad.net/bugs/1467239)
- Uncategorized : add 'backup on restore' option to confirm dialog
- Uncategorized : add check-config command for command-line
- Uncategorized : rewrite command-line argument parsing. Now using argparse
- Uncategorized : add expert option SSH command prefix

## 1.1.6 (2015-06-27)

### Uncategorized

- Uncategorized : show Profile name in systrayicon menu
- Uncategorized : make own Exceptions a childclass from BackInTimeException
- Uncategorized : remove consolekit from dependencies
- Specifying the SSH private key whenever ssh is called (https : //launchpad.net/bugs/1433682)
- add to in-/exclude directly from mainwindow (https : //launchpad.net/bugs/1454856)
- add option to run Smart Remove in background on remote host (https : //launchpad.net/bugs/1457210)
- Uncategorized : Use current profile when starting GUI from Systray

### Fixed

- encrypted remote backup hangs on 'start encfsctl encode process' (https://launchpad.net/bugs/1455925)
- missing profile<N>.name crashed GUI
- Segmentation fault caused by two QApplication instances (https://launchpad.net/bugs/1463732)
- no Changes [C] log entries with 'Check for changes' disabled (https://launchpad.net/bugs/1463367)
- some changed options from Settingsdialog where not respected during automatic tests after hitting OK
- python version check fails on python 3.3 (https://launchpad.net/bugs/1463686)
- pw-cache didn't start on Mint KDE because of missing stdout and stderr (https://launchpad.net/bugs/1431305)
- failed to restore file names with white spaces using CLI (https://launchpad.net/bugs/1435602)
- UnboundLocalError with 'last_snapshot' in _free_space (https://launchpad.net/bugs/1437623)

## 1.1.4 (2015-03-22)

### Uncategorized

- add option to keep new snapshot with 'full rsync mode' regardless of changes (https : //launchpad.net/bugs/1434722)
- remove base64 encoding for passwords as it doesn't add any security but broke the password process (https : //launchpad.net/bugs/1431305)
- add confirm dialog before restoring (https : //launchpad.net/bugs/438079)
- Uncategorized : add option to run only one snapshot at a time
- cache uuid in config so it doesn't fail if the device isn't plugged in (https : //launchpad.net/bugs/1426881)
- Uncategorized : add warning about wrong Python version in configure
- prevent snapshots from being removed with restore and delete; show warning if restore and delete filesystem root (https : //answers.launchpad.net/questions/262837)
- Uncategorized : add bash-completion
- use 'crontab' instead of 'crontab -' to read from stdin (https : //launchpad.net/bugs/1419466)

### Fixed

- wrong quote in 'Save config file'
- Deleting the last snapshot does not update the last_snapshot symlink (https://launchpad.net/bugs/1434724)
- Wrong status text in the tray icon (https://launchpad.net/bugs/1429400)
- restore permissions of lots of files made BackInTime unresponsive (https://launchpad.net/bugs/1428423)
- failed to restore file owner and group
- OSError in free_space; add alternate method to get free space
- ugly theme while running as root on Gnome based DEs (https://launchpad.net/bugs/1418447)
- UnicodeError thrown if filename has broken charset (https://launchpad.net/bugs/1419694)

## 1.1.2 (2015-02-04)

### Uncategorized

- Uncategorized : sort 'Backup folders' in main window
- Uncategorized : save in- and exclude sort order
- Uncategorized : use PolicyKit to install Udev rules
- Uncategorized : move compression from install to build in Makefiles
- Uncategorized : use pkexec to start backintime-qt4 as root

## 1.1.0 (2015-01-15)

### Uncategorized

- Uncategorized : add tooltips for rsync options
- Uncategorized : make only one debian/control
- multiselect files to restore (https : //launchpad.net/bugs/1135886)
- force run manual snapshots on battery (https : //launchpad.net/bugs/861553)
- Uncategorized : backup encfs config to local config folder
- Uncategorized : apply 'install-docs-move.patch' from Debian package by Jonathan Wiltshire
- add restore option to delete new files during restore (https : //launchpad.net/bugs/1371951)
- Uncategorized : use flock to prevent two instances running at the same time
- restore config dialog added (https : //launchpad.net/bugs/480391)
- Uncategorized : inhibit suspend/hibernate while take_snapshot or restore
- Uncategorized : use more reliable code for get_user
- Uncategorized : implement anacrons functions inside BIT => more flexible schedules and no new timestamp if there was an error
- Uncategorized : automatically run in background if started with 'backintime --backup-job'
- fix typos and style warnings in manpages reported by Lintian (https : //lintian.debian.org/full/jmw@debian.org.html#backintime_1.0.34-0.1)
- add exclude files by size (https : //launchpad.net/bugs/823719)
- Uncategorized : remove 'Auto Host/User/Profile-ID' as this is more confusing than helping
- optional run 'rsync' with 'nocache' (https : //launchpad.net/bugs/1344528)
- Uncategorized : mark invalid exclude pattern with mode ssh-encrypted
- Uncategorized : make Settingsdialog tabs scrollable
- remove colon ( : ) restriction in exclude pattern
- Uncategorized : prevent starting new snapshot if restore is running
- add top-level directory for tarball (https : //launchpad.net/bugs/1359076)
- Uncategorized : add more user-callback events (on App start and exit, on mount and unmount)
- Uncategorized : add context menu to files view
- Uncategorized : remove snapshots from commandline
- Uncategorized : multi selection in timeline => remove multiple snapshots with one click
- Uncategorized : print warning if started with sudo
- Uncategorized : add more default exclude; remove [Cc]ache* from exclude
- Uncategorized : add option for custom rsync-options
- Uncategorized : add ProgressBar for rsync
- Uncategorized : add progress for smart-remove
- Uncategorized : remove old status-bar message after a snapshot crashed.
- ask to include symlinks target instead link (https : //launchpad.net/bugs/1117709)
- Uncategorized : port to Python 3.x
- returncode >0 if there was an error (https : //launchpad.net/bugs/1040995)
- Uncategorized : Enable user-callback script to cancel a backup by returning a non-zero exit code.
- Uncategorized : merge backintime-notify into backintime-qt4
- Uncategorized : add --gksu/--gksudo arg to qt4/configure
- remember last path for each profile (https : //bugs.launchpad.net/bugs/1254870)
- sort include and exclude list (https : //bugs.launchpad.net/bugs/1193149)
- Uncategorized : Timeline show tooltip 'Last check'
- show hidden files in FileDialog (https : //bugs.launchpad.net/backintime/+bug/995925)
- add button text for all buttons (https : //bugs.launchpad.net/backintime/+bug/992020)
- add shortcuts (https : //bugs.launchpad.net/backintime/+bug/686694)
- add menubar (https : //bugs.launchpad.net/backintime/+bug/528851)
- Uncategorized : port KDE4 GUI to pure Qt4 to replace both KDE4 and Gnome GUI

### Fixed

- check procname of pid-locks (https://launchpad.net/bugs/1341414)
- Port check failed on IPv6 (https://launchpad.net/bugs/1361634)
- 'inotify_add_watch failed' while closing BIT
- systray icon didn't show up (https://bugs.launchpad.net/backintime/+bug/658424)

## 1.0.40 (2014-11-02)

### Uncategorized

- use fingerprint to check if ssh key was unlocked correctly (https : //answers.launchpad.net/questions/256408)
- add fallback method to get UUID (https : //answers.launchpad.net/questions/254140)

### Fixed

- 'Attempt to unlock mutex that was not locked'... this time for good

## 1.0.38 (2014-10-01)

### Fixed

- 'Attempt to unlock mutex that was not locked' in gnomeplugin (https://answers.launchpad.net/questions/255225)
- housekeeping by gnome-session-daemon might delete backup and original data (https://bugs.launchpad.net/bugs/1374343)
- Type Error in 'backintime --decode' (https://bugs.launchpad.net/bugs/1365072)
- take_snapshot didn't wait for snapshot folder come available if notifications are disabled (https://bugs.launchpad.net/bugs/1332979)

### Uncategorized

- Uncategorized : compare os.path.realpath instead of os.stat to get devices UUID

## 1.0.36 (2014-08-06)

### Uncategorized

- remove UbuntuOne from exclude (https : //bugs.launchpad.net/bugs/1340131)
- Gray out 'Add Profile' if 'Main Profile' isn't configured yet (https : //bugs.launchpad.net/bugs/1335545)
- Uncategorized : Don't check for fuse group-membership if group doesn't exist
- Uncategorized : disable keyring for root

### Fixed

- backintime-kde4 as root failed to load ssh-key (https://bugs.launchpad.net/bugs/1276348)
- kdesystrayicon.py crashes because of missing environ (https://bugs.launchpad.net/bugs/1332126)
- OSError if sshfs/encfs is not installed (https://bugs.launchpad.net/bugs/1316288)
- TypeError in config.py check_config() (https://bugzilla.redhat.com/show_bug.cgi?id=1091644)
- unhandled exception in create_last_snapshot_symlink() (https://bugs.launchpad.net/bugs/1269991)

## 1.0.34 (2013-12-21)

### Uncategorized

- sync/flush all disks before shutdown (https : //bugs.launchpad.net/bugs/1261031)

### Fixed

- BIT running as root shutdown after snapshot, regardless of option checked (https://bugs.launchpad.net/bugs/1261022)

## 1.0.32 (2013-12-13)

### Fixed

- cron scheduled snapshots won't start with 1.0.30

## 1.0.30 (2013-12-12)

### Uncategorized

- Uncategorized : scheduled and manual snapshots use --config
- make configure scripts portable (https : //bugs.launchpad.net/backintime/+bug/377429)
- add symlink last_snapshot (https : //bugs.launchpad.net/backintime/+bug/787118)
- Uncategorized : add virtual package backintime-kde for PPA
- Uncategorized : Fix multiple errors in PPA build process; reorganize updateversion.sh
- add option to run rsync with 'nice' or 'ionice' on remote host (https : //bugs.launchpad.net/backintime/+bug/1240301)
- add Shutdown button to shutdown system after snapshot has finished (https : //bugs.launchpad.net/backintime/+bug/838742)
- Uncategorized : wrap long lines for syslog

### Fixed

- udev rule doesn't finish (https://bugs.launchpad.net/backintime/+bug/1249466)
- Mate and xfce desktop didn't show systray icon (https://bugs.launchpad.net/backintime/+bug/658424/comments/31)
- Ubuntu Lucid doesn't provide SecretServiceKeyring (https://bugs.launchpad.net/backintime/+bug/1243911)
- 'gksu backintime-gnome' failed with dbus.exceptions.DBusException

## 1.0.28 (2013-10-19)

### Uncategorized

- Uncategorized : remove config on 'apt-get purge'
- Uncategorized : add more options for configure scripts; update README
- Uncategorized : add udev schedule (run BIT as soon as the drive is connected)
- add '--checksum' commandline option (https : //bugs.launchpad.net/backintime/+bug/886021)
- multi selection for include and exclude list (https : //bugs.launchpad.net/backintime/+bug/660753)

### Fixed

- AttributeError with python-keyring>1.6.1 (https://bugs.launchpad.net/backintime/+bug/1234024)
- TypeError: KDirModel.removeColumns() is a private method in kde4/app.py (https://bugs.launchpad.net/backintime/+bug/1232694)
- sshfs mount disconnect after a while due to some firewalls (add ServerAliveInterval) (https://answers.launchpad.net/backintime/+question/235685)
- Ping fails if ICMP is disabled on remote host (https://bugs.launchpad.net/backintime/+bug/1226718)
- KeyError in getgrnam if there is no 'fuse' group (https://bugs.launchpad.net/backintime/+bug/1225561)
- anacrontab won't work with profilename with spaces (https://bugs.launchpad.net/backintime/+bug/1224620)
- NameError in tools.move_snapshots_folder (https://bugs.launchpad.net/backintime/+bug/871466)
- KPassivePopup is not defined (https://bugs.launchpad.net/backintime/+bug/871475)
- ValueError while reading pw-cache PID (https://answers.launchpad.net/backintime/+question/235407)

## 1.0.26 (2013-09-07)

### Uncategorized

- add feature : keep min free inodes
- roll back commit 836.1.5 (check free-space on ssh remote host) : statvfs DOES work over sshfs. But not with quite outdated sshd
- Uncategorized : add daily anacron schedule
- Uncategorized : add delete button and 'list only equal' in Snapshot dialog; multiSelect in snapshot list
- Uncategorized : add manpage backintime-config and config-examples
- add feature : restore from command line; add option --config
- Uncategorized : use 'ps ax' to check if 'backintime --pw-cache' is still running
- Uncategorized : mount after locking, unmount before unlocking in take_snapshot
- Uncategorized : add option --bwlimit for rsync
- Uncategorized : redirect logger.error and .warning to stderr; new argument --quiet
- Uncategorized : deactivate 'Save Password' if no keyring is available
- Uncategorized : use Password-cache for user-input too
- Uncategorized : handle two Passwords
- add 'SSH encrypted' : mount / with encfs reverse and sync encrypted with rsync. EXPERIMENTAL!
- add 'Local encrypted' : mount encfs

### Fixed

- Restore makes files public during the operation
- Cannot keep modifications to cron (https://bugs.launchpad.net/backintime/+bug/698106)
- cannot stat 'backintime-kde4-root.desktop.kdesudo' (https://bugs.launchpad.net/backintime/+bug/696659)
- unreadable dark KDE color schemes (https://bugs.launchpad.net/backintime/+bug/1184920)
- permission denied if remote uid wasn't the same as local uid

## 1.0.24 (2013-05-08)

### Uncategorized

- Uncategorized : hide check_for_canges if full_rsync_mode is checked
- Uncategorized : DEFAULT_EXCLUDE system folders with /foo/* so at least the folder itself will backup
- Uncategorized : DEFAULT_EXCLUDE /run; exclude MOUNT_ROOT with higher priority and not with DEFAULT_EXCLUDE anymore
- Uncategorized : 'Save Password' default off to avoid problems with existing profiles
- Uncategorized : if restore uid/gid failed try to restore at least gid
- Uncategorized : SSH need to store permissions in separate file with "Full rsync mode" because remote user might not be able to store ownership
- switch to 'find -exec cmd {} +' (https : //bugs.launchpad.net/backintime/+bug/1157639)
- Uncategorized : change all indent tabs to 4 spaces

### Fixed

- 'CalledProcessError' object has no attribute 'strerror'
- quote rsync remote path with spaces
- restore permission failed on "Full rsync mode"
- glib.GError: Unknown internal child: selection
- GtkWarning: Unknown property: GtkLabel.margin-top
- check keyring backend only if password is needed

## 1.0.22 (2013-03-26)

### Uncategorized

- Uncategorized : check free-space on ssh remote host (statvfs didn't work over sshfs)
- Uncategorized : Add Password storage mode ssh
- Uncategorized : Add "Full rsync mode" (can be faster but ...)

### Fixed

- "Restore to..." failed due to spaces in directory name (https://bugs.launchpad.net/backintime/+bug/1096319)
- host not found in known_hosts if port != 22 (https://bugs.launchpad.net/backintime/+bug/1130356)
- sshtools.py used not POSIX conform conditionals

## 1.0.20 (2012-12-15)

### Fixed

- restore remote path with spaces using mode ssh returned error

## 1.0.18 (2012-11-17)

### Uncategorized

- Fix packages : man & translations
- Uncategorized : Map multiple arguments for gettext so they can be rearranged by translators

### Fixed

- https://bugs.launchpad.net/backintime/+bug/1077446
- https://bugs.launchpad.net/backintime/+bug/1078979
- https://bugs.launchpad.net/backintime/+bug/1079479

## 1.0.16 (2012-11-15)

### Uncategorized

- Fix a package dependency problem ... this time for good (https : //bugs.launchpad.net/backintime/+bug/1077446)

## 1.0.14 (2012-11-09)

### Uncategorized

- Uncategorized : Fix a package dependency problem

## 1.0.12 (2012-11-08)

### Uncategorized

- Add links to : website, documentation, report a bug, answers, faq
- Uncategorized : Use libnotify for gnome/kde4 notifications instead of gnome specific libraries
- Add more schedule options : every 30 min, every 2 hours, every 4 hours, every 6 hours & every 12 hours
- Uncategorized : Add generic mount-framework
- Uncategorized : Add mode 'SSH' for backups on remote host using ssh protocol.

### Fixed

- https://bugs.launchpad.net/backintime/+bug/1059247
- wrong path if restore system root
- glade (xml) files did not translate
- https://bugs.launchpad.net/backintime/+bug/1073867

## 1.0.10 (2012-03-06)

### Uncategorized

- Uncategorized : Add "Restore to ..." in replacement of copy (with or without drag & drop) because copy don't restore user/group/rights

## 1.0.8 (2011-06-18)

### Fixed

- https://bugs.launchpad.net/backintime/+bug/723545
- https://bugs.launchpad.net/backintime/+bug/705237
- https://bugs.launchpad.net/backintime/+bug/696663
- https://bugs.launchpad.net/backintime/+bug/671946

## 1.0.6 (2011-01-02)

### Fixed

- https://bugs.launchpad.net/backintime/+bug/676223
- https://bugs.launchpad.net/backintime/+bug/672705

### Uncategorized

- Smart remove : configurable options (https://bugs.launchpad.net/backintime/+bug/406765)

## 1.0.4 (2010-10-28)

### Uncategorized

- SettingsDialog : show highly recommended excludes
- Option to use checksum to detect changes (https : //bugs.launchpad.net/backintime/+bug/666964)
- Option to select log verbosity (https : //bugs.launchpad.net/backintime/+bug/664423)
- Gnome : use gloobus-preview if installed

### Fixed

- https://bugs.launchpad.net/backintime/+bug/664783

## 1.0.2 (2010-10-16)

### Uncategorized

- Uncategorized : reduce log file (no more duplicate "Compare with..." lines)
- Uncategorized : declare backintime-kde4 packages as a replacement of backintime-kde

## 1.0 (2010-10-16)

### Uncategorized

- add '.dropbox*' to default exclude patterns (https : //bugs.launchpad.net/backintime/+bug/628172)
- add option to take a snapshot at every boot (https : //bugs.launchpad.net/backintime/+bug/621810)
- Uncategorized : fix xattr
- add continue on errors (https : //bugs.launchpad.net/backintime/+bug/616299)
- add expert options : copy unsafe links & copy links
- Uncategorized : "user-callback" replace "user.callback" and receive profile information
- documentation : on-line only (easier to maintain)
- Uncategorized : add error log and error log view dialog (Gnome & KDE4)
- merge with : lp:~dave2010/backintime/minor-edits
- merge with : lp:~mcfonty/backintime/unique-snapshots-view
- Uncategorized : reduce memory usage during compare with previous snapshot process
- custom backup hour (for daily backups or mode) : https://bugs.launchpad.net/backintime/+bug/507451
- smart remove was slightly changed (https : //bugs.launchpad.net/backintime/+bug/502435)
- Uncategorized : make backup on restore optional
- Uncategorized : add ionice support for user/cron backup process
- fix bug that could cause "ghost" folders in snapshots (LP : 406092)
- fix bug that converted / into // (LP : #455149)
- remove "schedule per included directory" (profiles do that) (+ bug LP : #412470)
- fig bug : https://bugs.launchpad.net/backintime/+bug/489380
- Uncategorized : update Slovak translation (Tomáš Vadina <kyberdev@gmail.com>)
- Uncategorized : multiple profiles support
- GNOME : fix notification
- Uncategorized : backintime snapshot folder is restructured to ../backintime/machine/user/profile_id/
- Uncategorized : added the possibility to include other snapshot folders within a profile, it can only read those, there is not a GUI implementation yet
- Uncategorized : added a tag suffix to the snapshot_id, to avoid double snapshot_ids
- added a desktop file for kdesu and a test if kdesu or kdesudo should be used (LP : #389988)
- added expert option to disable snapshots when on battery (LP : #388178)
- fix bug handling big files by the GNOME GUI (LP : #409130)
- fix bug in handling of & characters by GNOME GUI (LP : #415848)
- fix a security bug in chmods before snapshot removal (LP : #419774)
- snapshots are stored entirely read-only (LP : #386275)
- fix exclude patterns in KDE4 (LP : #432537)
- fix opening german files with external applications in KDE (LP : #404652)
- changed default exclude patterns to caches, thumbnails, trashbins, and backups (LP : #422132)
- write access to snapshot folder is checked & change to snapshot version 2 (LP : #423086)
- fix small bugs (a.o. LP : #474307)
- Used a more standard crontab syntax (LP : #409783)
- Stop the "Over zealous removal of crontab entries" (LP : #451811)

### Fixed

- https://bugs.launchpad.net/backintime/+bug/588841
- https://bugs.launchpad.net/backintime/+bug/588215
- https://bugs.launchpad.net/backintime/+bug/588393
- https://bugs.launchpad.net/backintime/+bug/426400
- https://bugs.launchpad.net/backintime/+bug/575022
- https://bugs.launchpad.net/backintime/+bug/571894
- https://bugs.launchpad.net/backintime/+bug/553441
- https://bugs.launchpad.net/backintime/+bug/550765
- https://bugs.launchpad.net/backintime/+bug/507246
- https://bugs.launchpad.net/backintime/+bug/538855
- https://bugs.launchpad.net/backintime/+bug/386230
- https://bugs.launchpad.net/backintime/+bug/527039
- https://bugs.launchpad.net/backintime/+bug/520956
- https://bugs.launchpad.net/backintime/+bug/520930
- https://bugs.launchpad.net/backintime/+bug/521223
- https://bugs.launchpad.net/backintime/+bug/516066
- https://bugs.launchpad.net/backintime/+bug/512813
- https://bugs.launchpad.net/backintime/+bug/503859
- https://bugs.launchpad.net/backintime/+bug/501285
- https://bugs.launchpad.net/backintime/+bug/493558
- https://bugs.launchpad.net/backintime/+bug/441628
- https://bugs.launchpad.net/backintime/+bug/489319
- https://bugs.launchpad.net/backintime/+bug/447841
- https://bugs.launchpad.net/backintime/+bug/412695

## 0.9.26 (2009-05-19)

### Uncategorized

- Uncategorized : update translations from Launchpad
- Fix a bug in smart-remove algorithm (https : //bugs.launchpad.net/backintime/+bug/376104)
- Uncategorized : update German translation (Michael Wiedmann <mw@miwie.in-berlin.de>)
- Uncategorized : add '--no-check' option to configure scripts
- Uncategorized : use only 'folder' term (more consistent with GNOME/KDE)
- add 'expert option' : enable/disable nice for cron jobs
- GNOME & KDE4 : refresh snapshots button force files view to update too
- Uncategorized : you can include a backup parent directory (backup directory will auto-exclude itself)
- Uncategorized : fix some small bugs

### Fixed

- https://bugs.launchpad.net/backintime/+bug/374477
- https://bugs.launchpad.net/backintime/+bug/375113

## 0.9.24 (2009-05-07)

### Uncategorized

- Uncategorized : update translations
- KDE4 : fix python string <=> QString problems
- KDE4 FilesView/SnapshotsDialog : ctrl-click just select (don't execute)
- KDE4 : fix crush after "take snapshot" process (https://bugs.launchpad.net/backintime/+bug/366241)
- Uncategorized : store basic permission in a special file so it can restore them correctly (event from NTFS)
- Uncategorized : add config version
- Uncategorized : implement Gnome/KDE4 systray icons and user.callback as plugins
- reorganize code : common/GNOME/KDE4
- GNOME : break the big glade file in multiple file
- Uncategorized : backintime is no longer aware of 'backintime-gnome' and 'backintime-kde4'  

## 0.9.22.1 (2009-04-27)

### Uncategorized

- Uncategorized : fix French translation

## 0.9.22 (2009-04-24)

### Uncategorized

- Uncategorized : update translations from Launchpad
- KDE4 : fix some translation problems
- Uncategorized : remove --safe-links for save/restore (this means copy symlinks as symlinks)
- Uncategorized : update German translation (Michael Wiedmann <mw@miwie.in-berlin.de>)
- Uncategorized : create directory now use python os.makedirs (replace use of mkdir command)
- KDE4 : fix a crush related to QString - python string conversion
- GNOME & KDE4 SettingsDialog : if schedule automatic backups per directory is set, global schedule is hidden
- GNOME FilesView : thread "*~" files (backup files) as hidden files
- GNOME : use gtk-preferences icon for SettingsDialog (replace gtk-execute icon)
- expert option : $XDG_CONFIG_HOME/backintime/user.callback (if exists) is called a different steps 
- add more command line options : --snapshots-list, --snapshots-list-path, --last-snapshot, --last-snapshot-path
- follow FreeDesktop directories specs :  
- new install system : use more common steps (./configure; make; sudo make install)

## 0.9.20 (2009-04-06)

### Uncategorized

- smart remove : fix an important bug and make it more verbose in syslog
- Uncategorized : update Spanish translation (Francisco Manuel García Claramonte <franciscomanuel.garcia@hispalinux.es>)

## 0.9.18 (2009-04-02)

### Uncategorized

- Uncategorized : update translations from Launchpad
- Uncategorized : update Slovak translation (Tomáš Vadina <kyberdev@gmail.com>)
- Uncategorized : update French translation (Michel Corps <mahikeulbody@gmail.com>)
- Uncategorized : update German translation (Michael Wiedmann <mw@miwie.in-berlin.de>)
- GNOME bugfix : fix a crush in files view for files with special characters (ex: "a%20b")
- GNOME SettingsDialog bugfix : if snapshots path is a new created folder, snapshots navigation (files view) don't work
- Uncategorized : update doc
- GNOME & KDE4 MainWindow : Rename "Places" list with "Snapshots"
- GNOME SettingsDialog bugfix : modify something, then press cancel. If you reopen the dialog it show wrong values (the ones before cancel)
- GNOME & KDE4 : add root mode menu entries (use gksu for gnome and kdesudo for kde)
- GNOME & KDE4 : MainWindow - Files view: if the current directory don't exists in current snapshot display a message
- SettingDialog : add an expert option to enable to schedule automatic backups per directory
- SettingDialog : schedule automatic backups - if the application can't find crontab it show an error
- SettingDialog : if the application can't write in snapshots directory there should be an error message
- Uncategorized : add Polish translation (Paweł Hołuj <pholuj@gmail.com>)
- Uncategorized : add cron in common package dependencies
- GNOME & KDE4 : rework settings dialog
- SettingDialog : add an option to enable/disable notifications

## 0.9.16.1 (2009-03-16)

### Uncategorized

- Uncategorized : fix a bug/crush for French version

## 0.9.16 (2009-03-13)

### Uncategorized

- Uncategorized : update Spanish translation (Francisco Manuel García Claramonte <franciscomanuel.garcia@hispalinux.es>)
- Uncategorized : add Slovak translation (Tomáš Vadina <kyberdev@gmail.com>)
- Uncategorized : update Swedish translation (Niklas Grahn <terra.unknown@yahoo.com>)
- Uncategorized : update French translation (Michel Corps <mahikeulbody@gmail.com>)
- Uncategorized : update German translation (Michael Wiedmann <mw@miwie.in-berlin.de>)
- Uncategorized : update Slovenian translation (Vanja Cvelbar <cvelbar@gmail.com>)
- Uncategorized : don't show the snapshot that is being taken in snapshots list
- GNOME & KDE4 : when the application starts and snapshots directory don't exists show a messagebox
- Uncategorized : give more information for 'take snapshot' progress (to prove that is not blocked)
- MainWindow : rename 'Timeline' column with 'Snapshots'
- Uncategorized : when it tries to take a snapshot if the snapshots directory don't exists  
- GNOME & KDE4 : add notify if the snapshots directory don't exists
- KDE4 : rework MainWindow

## 0.9.14 (2009-03-05)

### Uncategorized

- Uncategorized : update German translation (Michael Wiedmann <mw@miwie.in-berlin.de>)
- Uncategorized : update Swedish translation (Niklas Grahn <terra.unknown@yahoo.com>)
- Uncategorized : update Spanish translation (Francisco Manuel García Claramonte <franciscomanuel.garcia@hispalinux.es>)
- Uncategorized : update French translation (Michel Corps <mahikeulbody@gmail.com>)
- GNOME & KDE4 : rework MainWindow
- GNOME & KDE4 : rework SettingsDialog
- GNOME & KDE4 : add "smart" remove

## 0.9.12 (2009-02-28)

### Fixed

- now if you include ".abc" folder and exclude ".*", ".abc" will be saved in the snapshot
- bookmarks with special characters

### Uncategorized

- KDE4 : add help
- Uncategorized : add Slovenian translation (Vanja Cvelbar <cvelbar@gmail.com>)

## 0.9.10 (2009-02-24)

### Uncategorized

- Uncategorized : add Swedish translation (Niklas Grahn <terra.unknown@yahoo.com>)
- KDE4 : drop and drop from backintime files view to any file manager

### Fixed

- fix a segfault when running from cron

## 0.9.8 (2009-02-20)

### Uncategorized

- Uncategorized : update Spanish translation (Francisco Manuel García Claramonte <franciscomanuel.garcia@hispalinux.es>)
- Uncategorized : unsafe links are ignored (that means that a link to a file/directory outside of include directories are ignored)
- KDE4 : add copy to clipboard
- KDE4 : sort files by name, size or date
- cron 5/10 minutes : replace multiple lines with a single crontab line using divide (*/5 or */10)
- cron : when called from cron redirect output (stdout & stderr) to /dev/null

### Fixed

- unable to restore files that contains space char in their name

## 0.9.6 (2009-02-09)

### Uncategorized

- Uncategorized : update Spanish translation (Francisco Manuel García Claramonte <franciscomanuel.garcia@hispalinux.es>)
- Uncategorized : update German translation (Michael Wiedmann <mw@miwie.in-berlin.de>)
- GNOME : update docbook
- KDE4 : add snapshots dialog
- GNOME & KDE4 : add update snapshots button
- GNOME : handle special folders icons (home, desktop)

## 0.9.4 (2009-01-30)

### Uncategorized

- Uncategorized : update German translation (Michael Wiedmann <mw@miwie.in-berlin.de>)
- gnome : better handling of 'take snapshot' status icon
- KDE4 (>= 4.1) : first version (not finished)
- Uncategorized : update man

## 0.9.2 (2009-01-16)

### Uncategorized

- Uncategorized : update Spanish translation (Francisco Manuel García Claramonte <franciscomanuel.garcia@hispalinux.es>)
- Uncategorized : update German translation (Michael Wiedmann <mw@miwie.in-berlin.de>)
- Uncategorized : replace diff with rsync to check if a new snapshot is needed
- Uncategorized : code cleanup
- Uncategorized : add show hidden & backup files toggle button for files view

### Fixed

- if you add "/a" in include directories and "/a/b" in exclude patterns, "/a/b*" items 
- it does not include ".*" items even if they are not excluded  

## 0.9 (2009-01-09)

### Uncategorized

- Uncategorized : update Spanish translation (Francisco Manuel García Claramonte <franciscomanuel.garcia@hispalinux.es>)
- Uncategorized : make deb packages more debian friendly (thanks to Michael Wiedmann <mw@miwie.in-berlin.de>)
- Uncategorized : update German translation (Michael Wiedmann <mw@miwie.in-berlin.de>)
- Uncategorized : better separation between common and gnome specific files and  
- Uncategorized : code cleanup

### Fixed

- when you open snapshots dialog for the second time ( or more ) and you make a diff  

## 0.8.20 (2008-12-22)

### Fixed

- sorting files/directories by name is now case insensitive

### Uncategorized

- getmessages.sh : ignore "gtk-" items (this are gtk stock item ids and should not be changed)

## 0.8.18 (2008-12-17)

### Uncategorized

- Uncategorized : update man/docbook
- Uncategorized : add sort columns in MainWindow/FileView (by name, by size or by date) and SnapshotsDialog (by date)
- Uncategorized : fix German translation (Michael Wiedmann <mw@miwie.in-berlin.de>)

## 0.8.16 (2008-12-11)

### Uncategorized

- add Drag & Drop from MainWindow : FileView/SnapshotsDialog to Nautilus
- Uncategorized : update German translation (Michael Wiedmann <mw@miwie.in-berlin.de>)

## 0.8.14 (2008-12-07)

### Uncategorized

- Uncategorized : add more command line parameters ( --version, --snapshots, --help )
- Uncategorized : fix a crush for getting info on dead symbolic links
- when taking a new backup based on the previous one don't copy the previous extra info (ex : name)
- Uncategorized : copy unsafe links when taking a snapshot

## 0.8.12 (2008-12-01)

### Uncategorized

- Uncategorized : add German translation (Michael Wiedmann <mw@miwie.in-berlin.de>)
- Uncategorized : add SnapshotNameDialog
- Uncategorized : add Name/Remove snapshot in main toolbar
- Uncategorized : change the way it detects if the mainwindow is the active window (no dialogs)
- toolbars : show icons only
- Uncategorized : update Spanish translation (Francisco Manuel García Claramonte <franciscomanuel.garcia@hispalinux.es>)

## 0.8.10 (2008-11-22)

### Uncategorized

- SnapshotsDialog : add right-click popup-menu and a toolbar with copy & restore buttons
- Uncategorized : use a more robust backup lock file
- Uncategorized : log using syslog
- Uncategorized : fix a small bug in copy to clipboard
- Uncategorized : update Spanish translation (Francisco Manuel García Claramonte <franciscomanuel.garcia@hispalinux.es>)

## 0.8.8 (2008-11-19)

### Uncategorized

- SnapshotsDialog : add diff
- Uncategorized : update Spanish translation (Francisco Manuel García Claramonte <franciscomanuel.garcia@hispalinux.es>)

## 0.8.6 (2008-11-17)

### Uncategorized

- Uncategorized : fix change backup path crush
- Uncategorized : add SnapshotsDialog

## 0.8.2 (2008-11-14)

### Uncategorized

- add right-click menu in files list : open (using gnome-open), copy (you can paste in Nautilus), restore (for snapshots only)
- Uncategorized : add Copy toolbar button for files list

## 0.8.1 (2008-11-10)

### Uncategorized

- Uncategorized : add every 5/10 minutes automatic backup

## 0.8 (2008-11-07)

### Uncategorized

- Uncategorized : don't show backup files (*~)
- Uncategorized : add backup files to default exclude patterns (*~)
- makedeb.sh : make a single package with all languages included
- install.sh : install all languages
- Uncategorized : add English manual (man)
- Uncategorized : add English help (docbook)
- Uncategorized : add help button in main toolbar
- Uncategorized : the application can be started with a 'path' to a folder or file as command line parameter
- Uncategorized : when the application start, if it is already running pass its command line to the first instance (this allow a basic integration with file-managers - see README)

### Fixed

- when the application was started a second time it raise the first application's window but not always focused

## 0.7.4 (2008-11-03)

### Uncategorized

- Uncategorized : if there is already a GUI instance running raise it
- Uncategorized : add Spanish translation (Francisco Manuel García Claramonte <franciscomanuel.garcia@hispalinux.es>)

## 0.7.2 (2008-10-28)

### Uncategorized

- Uncategorized : better integration with gnome icons (use mime-types)
- Uncategorized : remember last path
- Uncategorized : capitalize month in timeline (bug in french translation)

## 0.7 (2008-10-22)

### Uncategorized

- Uncategorized : fix cron segfault
- Uncategorized : fix a crush when launched the very first time (not configured)
- Uncategorized : multi-lingual support
- Uncategorized : add French translation

## 0.6.4 (2008-10-20)

### Uncategorized

- Uncategorized : remove About & Settings dialogs from the pager
- Uncategorized : allow only one instance of the application

## 0.6.2 (2008-10-16)

### Uncategorized

- Uncategorized : remember window position & size

## 0.6 (2008-10-13)

### Uncategorized

- Uncategorized : when it make a snapshot it display an icon in systray area
- Uncategorized : the background color for group items in timeline and places reflect more 
- Uncategorized : during restore only restore button is grayed ( even if everything is blocked )

## 0.5.1 (2008-10-10)

### Uncategorized

- Uncategorized : add size & date columns in files view
- Uncategorized : changed some texts

## 0.5 (2008-10-03)

### Uncategorized

- Uncategorized : This is the first release.

[1.4.4-dev]: https://github.com/bit-team/backintime/releases/tag/v1.4.4-dev
[1.4.3]: https://github.com/bit-team/backintime/releases/tag/v1.4.3
[1.4.1]: https://github.com/bit-team/backintime/releases/tag/v1.4.1
[1.4.0]: https://github.com/bit-team/backintime/releases/tag/v1.4.0
[1.3.3]: https://github.com/bit-team/backintime/releases/tag/v1.3.3
[1.3.2]: https://github.com/bit-team/backintime/releases/tag/v1.3.2
[1.3.1]: https://github.com/bit-team/backintime/releases/tag/v1.3.1
[1.3.0]: https://github.com/bit-team/backintime/releases/tag/v1.3.0
[1.2.1]: https://github.com/bit-team/backintime/releases/tag/v1.2.1
[1.2.0]: https://github.com/bit-team/backintime/releases/tag/v1.2.0
[1.1.24]: https://github.com/bit-team/backintime/releases/tag/v1.1.24
[1.1.22]: https://github.com/bit-team/backintime/releases/tag/v1.1.22
[1.1.20]: https://github.com/bit-team/backintime/releases/tag/v1.1.20
[1.1.18]: https://github.com/bit-team/backintime/releases/tag/v1.1.18
[1.1.16]: https://github.com/bit-team/backintime/releases/tag/v1.1.16
[1.1.14]: https://github.com/bit-team/backintime/releases/tag/v1.1.14
[1.1.12]: https://github.com/bit-team/backintime/releases/tag/v1.1.12
[1.1.10]: https://github.com/bit-team/backintime/releases/tag/v1.1.10
[1.1.8]: https://github.com/bit-team/backintime/releases/tag/v1.1.8
[1.1.6]: https://github.com/bit-team/backintime/releases/tag/v1.1.6
[1.1.4]: https://github.com/bit-team/backintime/releases/tag/v1.1.4
[1.1.2]: https://github.com/bit-team/backintime/releases/tag/v1.1.2
[1.1.0]: https://github.com/bit-team/backintime/releases/tag/v1.1.0
[1.0.40]: https://github.com/bit-team/backintime/releases/tag/v1.0.40
[1.0.38]: https://github.com/bit-team/backintime/releases/tag/v1.0.38
[1.0.36]: https://github.com/bit-team/backintime/releases/tag/v1.0.36
[1.0.34]: https://github.com/bit-team/backintime/releases/tag/v1.0.34
[1.0.32]: https://github.com/bit-team/backintime/releases/tag/v1.0.32
[1.0.30]: https://github.com/bit-team/backintime/releases/tag/v1.0.30
[1.0.28]: https://github.com/bit-team/backintime/releases/tag/v1.0.28
[1.0.26]: https://github.com/bit-team/backintime/releases/tag/v1.0.26
[1.0.24]: https://github.com/bit-team/backintime/releases/tag/v1.0.24
[1.0.22]: https://github.com/bit-team/backintime/releases/tag/v1.0.22
[1.0.20]: https://github.com/bit-team/backintime/releases/tag/v1.0.20
[1.0.18]: https://github.com/bit-team/backintime/releases/tag/v1.0.18
[1.0.16]: https://github.com/bit-team/backintime/releases/tag/v1.0.16
[1.0.14]: https://github.com/bit-team/backintime/releases/tag/v1.0.14
[1.0.12]: https://github.com/bit-team/backintime/releases/tag/v1.0.12
[1.0.10]: https://github.com/bit-team/backintime/releases/tag/v1.0.10
[1.0.8]: https://github.com/bit-team/backintime/releases/tag/v1.0.8
[1.0.6]: https://github.com/bit-team/backintime/releases/tag/v1.0.6
[1.0.4]: https://github.com/bit-team/backintime/releases/tag/v1.0.4
[1.0.2]: https://github.com/bit-team/backintime/releases/tag/v1.0.2
[1.0]: https://github.com/bit-team/backintime/releases/tag/v1.0
[0.9.26]: https://github.com/bit-team/backintime/releases/tag/v0.9.26
[0.9.24]: https://github.com/bit-team/backintime/releases/tag/v0.9.24
[0.9.22.1]: https://github.com/bit-team/backintime/releases/tag/v0.9.22.1
[0.9.22]: https://github.com/bit-team/backintime/releases/tag/v0.9.22
[0.9.20]: https://github.com/bit-team/backintime/releases/tag/v0.9.20
[0.9.18]: https://github.com/bit-team/backintime/releases/tag/v0.9.18
[0.9.16.1]: https://github.com/bit-team/backintime/releases/tag/v0.9.16.1
[0.9.16]: https://github.com/bit-team/backintime/releases/tag/v0.9.16
[0.9.14]: https://github.com/bit-team/backintime/releases/tag/v0.9.14
[0.9.12]: https://github.com/bit-team/backintime/releases/tag/v0.9.12
[0.9.10]: https://github.com/bit-team/backintime/releases/tag/v0.9.10
[0.9.8]: https://github.com/bit-team/backintime/releases/tag/v0.9.8
[0.9.6]: https://github.com/bit-team/backintime/releases/tag/v0.9.6
[0.9.4]: https://github.com/bit-team/backintime/releases/tag/v0.9.4
[0.9.2]: https://github.com/bit-team/backintime/releases/tag/v0.9.2
[0.9]: https://github.com/bit-team/backintime/releases/tag/v0.9
[0.8.20]: https://github.com/bit-team/backintime/releases/tag/v0.8.20
[0.8.18]: https://github.com/bit-team/backintime/releases/tag/v0.8.18
[0.8.16]: https://github.com/bit-team/backintime/releases/tag/v0.8.16
[0.8.14]: https://github.com/bit-team/backintime/releases/tag/v0.8.14
[0.8.12]: https://github.com/bit-team/backintime/releases/tag/v0.8.12
[0.8.10]: https://github.com/bit-team/backintime/releases/tag/v0.8.10
[0.8.8]: https://github.com/bit-team/backintime/releases/tag/v0.8.8
[0.8.6]: https://github.com/bit-team/backintime/releases/tag/v0.8.6
[0.8.2]: https://github.com/bit-team/backintime/releases/tag/v0.8.2
[0.8.1]: https://github.com/bit-team/backintime/releases/tag/v0.8.1
[0.8]: https://github.com/bit-team/backintime/releases/tag/v0.8
[0.7.4]: https://github.com/bit-team/backintime/releases/tag/v0.7.4
[0.7.2]: https://github.com/bit-team/backintime/releases/tag/v0.7.2
[0.7]: https://github.com/bit-team/backintime/releases/tag/v0.7
[0.6.4]: https://github.com/bit-team/backintime/releases/tag/v0.6.4
[0.6.2]: https://github.com/bit-team/backintime/releases/tag/v0.6.2
[0.6]: https://github.com/bit-team/backintime/releases/tag/v0.6
[0.5.1]: https://github.com/bit-team/backintime/releases/tag/v0.5.1
[0.5]: https://github.com/bit-team/backintime/releases/tag/v0.5

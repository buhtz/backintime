#!/usr/bin/env python3
import sys
import inspect
from pathlib import Path

# Workaround (see #1575)
sys.path.insert(0, str(SRC_PATH.parent))
import konfig
import version

VERSION = version.__version__
TIMESTAMP = strftime('%b %Y', gmtime())

HEADER = r'''.TH backintime-config 1 "{TIMESTAMP}" "version {VERSION}" "USER COMMANDS"
.SH NAME
config \- BackInTime configuration files.
.SH SYNOPSIS
~/.config/backintime/config
.br
/etc/backintime/config
.SH DESCRIPTION
Back In Time was developed as pure GUI program and so most functions are only
usable with backintime-qt. But it is possible to use
Back In Time e.g. on a headless server. You have to create the configuration file
(~/.config/backintime/config) manually. Look inside /usr/share/doc/backintime\-common/examples/ for examples.
.PP
The configuration file has the following format:
.br
keyword=arguments
.PP
Arguments don't need to be quoted. All characters are allowed except '='.
.PP
Run 'backintime check-config' to verify the configfile, create the snapshot folder and crontab entries.
.SH POSSIBLE KEYWORDS
'''

FOOTER = r'''.SH SEE ALSO
backintime, backintime-qt.
.PP
Back In Time also has a website: https://github.com/bit-team/backintime
.SH AUTHOR
This manual page was written by the BIT Team(<bit-dev@python.org>).
'''



def _get_public_properties() -> tuple:
    """Extract the public properties from our target config class."""
    def _is_public_property(val):
        return (
            not val.startswith('_')
            and isinstance(getattr(konfig.Konfig, val), property)
        )

    return tuple(filter(_is_public_property, dir(konfig.Konfig)))

def lint_manpage() -> bool:
    """
    LC_ALL=C.UTF-8 MANROFFSEQ='' MANWIDTH=80 man --warnings -E UTF-8 -l -Tutf8 -Z <file> >/dev/null
    """
    return False

def main():
    for prop in _get_public_properties():
        attr = getattr(konfig.Konfig, prop)

        # Ignore properties without docstring
        if not attr.__doc__:
            print('Missing docstring for "{prop}". Ignoring it.')
            continue

        print(f'Public property: {prop}')
        print(attr.__doc__)


if __name__ == '__main__':
    main()

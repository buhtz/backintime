#!/usr/bin/env python3
import sys
import inspect
from pathlib import Path

SRC_PATH = Path.cwd() / 'common' / 'konfig.py'

# Workaround (see #1575)
sys.path.insert(0, str(SRC_PATH.parent))
import konfig

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

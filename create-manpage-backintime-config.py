#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2012-2022 Germar Reitze
# SPDX-FileCopyrightText: © 2024 Christian BUHTZ <c.buhtz@posteo.jp>
#
# SPDX-License-Identifier: GPL-2.0
#
# This file is part of the program "Back In Time" which is released under GNU
# General Public License v2 (GPLv2).
# See file LICENSE or go to <https://www.gnu.org/licenses/#GPL>.
"""This script is a helper to create a manpage about Back In Times's config
file.

The file `common/config.py` is parsed for variable names, default values and
other information. The founder of that script @Germar gave a detailed
description about that script in #1354.

The script reads every line and tries to analyze it:
  - It searches for `DEFAULT` and puts those into a `dict` for later replacing
    the variable with the value.
  - If that didn't match it will look for lines starting with `#?` which is
    basically my own description for the manpage-entry.
    Multiple lines will get merged and stored in `commentline` until the
    processing of the current config option is done. That will reset
    `commentline`.
  - If a line starts with `#` it will be skipped.
  - Next the script searches for lines which ``return`` the config value (like
    `snapshots.ssh.port`. There it will extract the
    key/name (`snapshots.ssh.port`), the default value (`22`),
    the instance (`Int`) and if it is a profile or general value.
  - If the line contains a `List` value like `snapshots.include` it will
    process all values for the list like `snapshots.include.<I>.value` and
    `snapshots.include.<I>.type`.  Also it will add the size like
    `snapshots.include.size`.

In `process_line` it will replace some information with those I wrote manually
in the `#?` description, separated by `;` there is the comment,  value,
force_default and force_var. If there is no forced value it will chose the
value based on the instance with `select_values`
"""
import os
import sys
import re
import inspect
import subprocess
import json
from pathlib import Path
from time import strftime, gmtime
from typing import Any
# Workaround (see #1575)
sys.path.insert(0, str(Path.cwd() / 'common'))
import konfig
import version

MAN = Path.cwd() / 'common' / 'man' / 'C' / 'backintime-config.1'

# Extract multiline string between { and the latest }
REX_DICT_EXTRACT = re.compile(r'\{([\s\S]*)\}')

# |--------------------------|
# | GNU Trof (groff) helpers |
# |--------------------------|

def groff_section(section: str) -> str:
    """Section header"""
    return f'.SH {section}\n'

def groff_indented_paragraph(label: str, indent: int=6) -> str:
    """.IP - Indented Paragraph"""
    return f'.IP "{label}" {indent}'

def groff_italic(text: str) -> str:
    """\\fi - Italic"""
    return f'\\fI{text}\\fR'

def groff_bold(text: str) -> str:
    """Bold"""
    return f'\\fB{text}\\fR'

def groff_bold_roman(text: str) -> str:
    """The first part of the text is marked bold the rest is
    roman/normal.

    Used to reference other man pages."""
    return f'.BR {text}\n'

def groff_indented_block(text: str) -> str:
    """
    .RS - Start indented block
    .RE - End indented block
    """
    return f'\n.RS\n{text}\n.RE\n'

def groff_linebreak() -> str:
    """.br - Line break"""
    return '.br\n'

def groff_paragraph_break() -> str:
    """.PP - Paragraph break"""
    return '.PP\n'

# |--------------------|
# | Content generation |
# |--------------------|

def header():
    stamp = strftime('%b %Y', gmtime())
    ver = version.__version__

    content = f'.TH backintime-config 1 "{stamp}" ' \
              f'"version {ver}" "USER COMMANDS"\n'

    content += groff_section('NAME')
    content += 'config \- Back In Time configuration file.\n'

    content += groff_section('SYNOPSIS')
    content += '~/.config/backintime/config\n'
    content += groff_linebreak()
    content += '/etc/backintime/config\n'

    content += groff_section('DESCRIPTION')
    content += 'Back In Time was developed as pure GUI program and so most ' \
               'functions are only usable with '
    content += groff_bold('backintime-qt')
    content += '. But it is possible to use Back In Time e.g. on a ' \
               'headless server. You have to create the configuration file ' \
               '(~/.config/backintime/config) manually. Look inside ' \
               '/usr/share/doc/backintime\-common/examples/ for examples.\n'

    content += groff_paragraph_break()
    content += 'The configuration file has the following format:\n'
    content += groff_linebreak()
    content += 'keyword=arguments\n'

    content += groff_paragraph_break()
    content += "Arguments don't need to be quoted. All characters are " \
               "allowed except '='.\n"

    content += groff_paragraph_break()
    content += "Run 'backintime check-config' to verify the configfile, " \
               "create the snapshot folder and crontab entries.\n"

    content += groff_section('POSSIBLE KEYWORDS')

    return content

def entry_to_groff(name: str, doc: str, values: Any, default: Any) -> None:
    """Generate GNU Troff (groff) markup code for the given config entry."""
    type_name = type(default).__name__

    ret = f'Type: {type_name:<10}Allowed Values: {values}\n'
    ret += groff_linebreak()
    ret += f'{doc}\n'
    ret += groff_paragraph_break()

    ret += f'Default: {default}'

    ret = groff_indented_block(ret)
    ret = groff_indented_paragraph(groff_italic(name)) + ret

    return ret

def footer() -> str:
    content = groff_section('SEE ALSO')
    content += groff_bold_roman('backintime (1),')
    content += groff_bold_roman('backintime-qt (1)')
    content += groff_paragraph_break()
    content += 'Back In Time also has a website: ' \
               'https://github.com/bit-team/backintime\n'

    content += groff_section('AUTHOR')
    content += 'This manual page was written by the ' \
               'Back In Time Team (<bit-dev@python.org>).'

    return content

# |------|
# | Misc |
# |------|

def _get_public_properties(cls: type) -> tuple:
    """Extract the public properties from our target config class."""
    def _is_public_property(val):
        return (
            not val.startswith('_')
            and isinstance(getattr(cls, val), property)
        )

    return tuple(filter(_is_public_property, dir(cls)))

def lint_manpage(path: Path) -> bool:
    """Lint the manpage the same way as the Debian Lintian does."""

    print('Linting man page...')

    cmd = [
        'man',
        '--warnings',
        '-E',
        'UTF-8',
        '-l',
        '-Tutf8',
        '-Z',
        str(path)
    ]

    env = dict(
        **os.environ,
        LC_ALL='C.UTF-8',
        # MANROFFSEQ="''",
        MANWIDTH='80',
    )

    try:
        with open('/dev/null', 'w') as devnull:
            result = subprocess.run(
                cmd,
                env=env,
                check=True,
                text=True,
                stdout=devnull,
                stderr=subprocess.PIPE
            )

    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f'Unexpected error: {exc.stderr=}') from exc

    # Report warnings
    if result.stderr:
        print(result.stderr)
        return False

    print('No problems reported')
    return True

def inspect_properties(cls: type):
    entries = {}

    # Each public property in the class
    for prop in _get_public_properties(cls):
        attr = getattr(cls, prop)

        # Ignore properties without docstring
        if not attr.__doc__:
            print(f'Ignoring "{cls.__name__}.{prop}" because of '
                  'missing docstring.')
            continue

        print(f'{cls.__name__}.{prop}')

        doc = attr.__doc__

        # extract the dict from docstring
        the_dict = REX_DICT_EXTRACT.search(doc).groups()[0]
        the_dict = '{' + the_dict + '}'

        # remove the dict from docstring
        doc = doc.replace(the_dict, '')

        # Make it a real dict
        the_dict = eval(the_dict)

        # Clean up the docstring from empty lines and other blanks
        doc = ' '.join(line.strip()
                       for line in
                       filter(lambda val: len(val.strip()), doc.split('\n')))

        # store the result
        the_dict['doc'] = doc
        entries[the_dict.pop('name')] = the_dict

    return entries


def main():
    """The classes `Konfig` and `Konfig.Profile` are inspected and relevant
    information is extracted to create a man page of it.

    Only public properties with doc strings are used. The doc strings also
    need to contain a with additional information.

    Example ::

        {
            'option.name': {
                'values': (0, 99999),
                'default': 0,
                'doc': 'description text',
            },
        }
    """

    global_entries = inspect_properties(konfig.Konfig)
    profile_entries = inspect_properties(konfig.Konfig.Profile)
    # # Each "global" public property
    # for prop in _get_public_properties(konfig.Konfig):
    #     attr = getattr(konfig.Konfig, prop)

    #     # Ignore properties without docstring
    #     if not attr.__doc__:
    #         print(f'Ignoring "{prop}" because of missing docstring.')
    #         continue

    #     doc = attr.__doc__

    #     # extract the dict
    #     the_dict = rex.search(doc).groups()[0]
    #     the_dict = '{' + the_dict + '}'
    #     # Remove dict-like string from the doc string
    #     doc = doc.replace(the_dict, '')
    #     # Remove empty lines and other blanks
    #     doc = ' '.join(line.strip()
    #                    for line in
    #                    filter(lambda val: len(val.strip()), doc.split('\n')))
    #     # Make it a real dict
    #     the_dict = eval(the_dict)
    #     the_dict['doc'] = doc

    #     # store the result
    #     entries[the_dict.pop('name')] = the_dict


    with MAN.open('w', encoding='utf-8') as handle:
        print(f'Write GNU Troff (groff) markup to "{MAN}".')
        handle.write(header())

        for name, entry in {**global_entries, **profile_entries}.items():
            handle.write(
                entry_to_groff(
                    name=name,
                    doc=entry['doc'],
                    values=entry['values'],
                    default=entry['default']
                )
            )
            handle.write('\n')

        handle.write(footer())
        handle.write('\n')

        print(f'Finished creating man page.')

    lint_manpage(MAN)

if __name__ == '__main__':
    main()

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
from pathlib import Path
from time import strftime, gmtime
# Workaround (see #1575)
sys.path.insert(0, str(Path.cwd() / 'common'))
import konfig
import version

# PATH = os.path.join(os.getcwd(), 'common')
# CONFIG = os.path.join(PATH, 'config.py')
MAN = Path.cwd() / 'common' / 'man' / 'C' / 'backintime-config.1'

# with open(os.path.join(PATH, '../VERSION'), 'r') as f:
#     VERSION = f.read().strip('\n')

SORT = True  # True = sort by alphabet; False = sort by line numbering

# c_list = re.compile(r'.*?self\.(?!set)((?:profile)?)(List)Value ?\( ?[\'"](.*?)[\'"], ?((?:\(.*\)|[^,]*)), ?[\'"]?([^\'",\)]*)[\'"]?')
# c = re.compile(r'.*?self\.(?!set)((?:profile)?)(.*?)Value ?\( ?[\'"](.*?)[\'"] ?(%?[^,]*?), ?[\'"]?([^\'",\)]*)[\'"]?')


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

INSTANCE = 'instance'
NAME = 'name'
VALUES = 'values'
DEFAULT = 'default'
COMMENT = 'comment'
REFERENCE = 'reference'
LINE = 'line'

def groff_indented_paragraph(label: str, indent: int=6) -> str:
    """.IP - Indented Paragraph"""
    return f'.IP "{label}" {indent}'

def groff_italic(text: str) -> str:
    """\\fi - Italic"""
    return f'\\fI{text}\\fR'

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


def entry_to_groff(instance='', name='', values='', default='',
           comment='', reference='', line=0):
    """Generate GNU Troff (groff) markup code for the given config entry."""
    if not default:
        default = "''"

    ret = f'Type: {instance.lower():<10}Allowed Values: {values}\n'
    ret += groff_linebreak()
    ret += f'{comment}\n'
    ret += groff_paragraph_break()

    if SORT:
        ret += f'Default: {default}'
    else:
        ret += f'Default: {default:<18} {reference} line: {line}'

    ret = groff_indented_block(ret)
    ret = groff_indented_paragraph(groff_italic(name)) + ret

    return ret


def select(a, b):
    if a:
        return a

    return b


def _DEPRECATED_select_values(instance, values):
    if values:
        return values

    return {
        'bool': 'true|false',
        'str': 'text',
        'int': '0-99999'
    }[instance.lower()]


def _DEPRECATED_process_line(d, key, profile, instance, name, var, default, commentline,
                 values, force_var, force_default, replace_default, counter):
    """Parsing the config.py Python code"""
    # Ignore commentlines with #?! and 'config.version'
    comment = None

    if not commentline.startswith('!') and key not in d:
        d[key] = {}
        commentline = commentline.split(';')

        try:
            comment = commentline[0]
            values = commentline[1]
            force_default = commentline[2]
            force_var = commentline[3]

        except IndexError:
            pass

        if default.startswith('self.') and default[5:] in replace_default:
            default = replace_default[default[5:]]

        if isinstance(force_default, str) \
           and force_default.startswith('self.') \
           and force_default[5:] in replace_default:
            force_default = replace_default[force_default[5:]]

        if instance.lower() == 'bool':
            default = default.lower()

        d[key][INSTANCE] = instance
        d[key][NAME] = re.sub(
            r'%[\S]', '<%s>' % select(force_var, var).upper(), name
        )
        d[key][VALUES] = select_values(instance, values)
        d[key][DEFAULT] = select(force_default, default)
        d[key][COMMENT] = re.sub(r'\\n', '\n.br\n', comment)
        d[key][REFERENCE] = 'config.py'
        d[key][LINE] = counter


def _get_public_properties(cls: type) -> tuple:
    """Extract the public properties from our target config class."""
    def _is_public_property(val):
        return (
            not val.startswith('_')
            and isinstance(getattr(cls, val), property)
        )

    return tuple(filter(_is_public_property, dir(konfig.Konfig)))

def lint_manpage() -> bool:
    """
    LC_ALL=C.UTF-8 MANROFFSEQ='' MANWIDTH=80 man --warnings -E UTF-8 -l -Tutf8 -Z <file> >/dev/null
    """
    return False


def main():
    # Extract multiline string between { and the latest }
    rex = re.compile(r'\{([\s\S]*)\}')

    entries = {}
    profile_entries = {}

    # Each "global" public property
    for prop in _get_public_properties(konfig.Konfig):
        attr = getattr(konfig.Konfig, prop)

        # Ignore properties without docstring
        if not attr.__doc__:
            print(f'Ignoring "{prop}" because of missing docstring.')
            continue

        print(f'Public property: {prop}')
        print(attr.__doc__)

        doc = attr.__doc__

        # extract the dict
        the_dict = rex.search(doc).groups()[0]
        the_dict = '{' + the_dict + '}'
        # Remove dict-like string from the doc string
        doc = doc.replace(the_dict, '')
        # Remove empty lines and other blanks
        doc = ' '.join(line.strip()
                       for line in
                       filter(lambda val: len(val.strip()), doc.split('\n')))
        # Make it a real dict
        the_dict = eval(the_dict)
        the_dict['doc'] = doc

        # store the result
        entries[the_dict.pop('name')] = the_dict

    import json
    print(json.dumps(entries, indent=4))

    # Each "profile" public property
    for prop in _get_public_properties(konfig.Konfig.Profile):
        attr = getattr(konfig.Konfig.Profile, prop)



    sys.exit()



    # d = {
    #     'profiles.version': {
    #         INSTANCE: 'int',
    #         NAME: 'profiles.version',
    #         VALUES: '1',
    #         DEFAULT: '1',
    #         COMMENT: 'Internal version of profiles config.',
    #         REFERENCE: 'configfile.py',
    #         LINE: 419
    #     },
    #     'profiles': {
    #         INSTANCE: 'str',
    #         NAME: 'profiles',
    #         VALUES: 'int separated by colon (e.g. 1:3:4)',
    #         DEFAULT: '1',
    #         COMMENT: 'All active Profiles (<N> in profile<N>.snapshots...).',
    #         REFERENCE: 'configfile.py',
    #         LINE: 472
    #     },
    #     'profile<N>.name': {
    #         INSTANCE: 'str',
    #         NAME: 'profile<N>.name',
    #         VALUES: 'text',
    #         DEFAULT: 'Main profile',
    #         COMMENT: 'Name of this profile.',
    #         REFERENCE: 'configfile.py',
    #         LINE: 704
    #     }
    # }

    """
    Example for content of 'd':
        {
            "profiles": {
            "instance": "str",
            "name": "profiles",
            "values": "int separated by colon (e.g. 1:3:4)",
            "default": "1",
            "comment": "All active Profiles (<N> in profile<N>.snapshots...).",
            "reference": "configfile.py",
            "line": 472
        },
        "profile<N>.name": {
            "instance": "str",
            "name": "profile<N>.name",
            "values": "text",
            "default": "Main profile",
            "comment": "Name of this profile.",
            "reference": "configfile.py",
            "line": 704
        }
    """
    with MAN.open('w', encoding='utf-8') as handle:
        print(f'Write GNU Troff (groff) markup to "{MAN}". {SORT=}')
        handle.write(HEADER)

        if SORT:
            # Sort by alphabet
            s = lambda x: x
        else:
            # Sort by line numbering (in the source file)
            s = lambda x: d[x][LINE]

        handle.write('\n'.join(
            entry_to_groff(**d[key])
            for key in sorted(d, key=s)
        ))

        handle.write(FOOTER)


if __name__ == '__main__':
    main()

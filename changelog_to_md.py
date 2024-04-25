#!/usr/bin/env python3
from collections import defaultdict
import re
from pathlib import Path


def main():
    result = []
    fp = Path('CHANGES')

    items = []

    all_lines = fp.read_text('utf-8').split('\n')
    # PLAUSI
    if not all_lines[0] == 'Back In Time' or not all_lines[1] == '':
        raise ValueError('Unexpected content.\n{all_lines[:4]}')

    def _append_items(items):
        if items:
            result[-1] = (result[-1][0], items[:])
            items = []

        return items

    for line in all_lines[2:]:
        # print(f'\n\n{result=}')
        # print(f'Processing line {line}...')
        # ignore empty lines
        if not line:
            continue

        # bullet point?
        if line[0] in ['*', '-', '+']:
            # new item
            items.append(line)
            continue

        # next line of a bullet point?
        if line[0] == ' ':
            # append to last item
            items[-1] = items[-1] + ' ' + line[0].strip()
            continue

        # everything else
        items = _append_items(items)

        result.append((line, []))

    _append_items(items)

    return result


def get_std_suffix(suffix):
    """
    '### Changed',
    '### Removed',
    """
    if suffix.upper() == 'UNKNOWN':
        return 'Unknown'

    fixed = (
        'FIX',
        'BUG FIX',
        'FIX BUG',
        'BACKPORT BUG FIX',
        'FIX CRITICAL BUG',
        'BUG FIX (GNOME)',
    )
    if suffix.upper() in fixed:
        return 'Fixed'

    added = ('FEATURE')
    if suffix.upper() in added:
        return 'Added'

    other = ()
    if suffix in other:
        return 'Uncategorized'

    return None


def process_items(items):
    result = defaultdict(list)

    rex_suffix = re.compile(r'^\*\s*([^:]+):\s*(.+)')

    for i in items:
        try:
            suffix, content = rex_suffix.search(i).groups()
        except AttributeError:
            suffix = 'Uncategorized'
            content = i[2:]  # cut bullet

        std_suffix = get_std_suffix(suffix)

        if std_suffix is None:
            content = suffix + ' : ' + content
            std_suffix = 'Uncategorized'

        result[std_suffix].append(content)

    return result


def process_raw_results(raw_result):
    result = []

    # Extract version and date
    rex_ver_date = re.compile(
        r'^Version (\d+\.\d+.*) \((.+)\)$')

    for heading, items in raw_result:
        # print(heading)
        # print(items)
        # print('------\n\n')
        # continue
        version, date = rex_ver_date.search(heading).groups()

        result.append(
            (
                version,
                date,
                process_items(items)
            )
        )

    return result


def to_markdown(data, fh):
    # reference links added to the end of the markdown File
    ref_links = []

    # Head
    fh.write('# Changelog\n')
    fh.write('[![Common Changelog](https://common-changelog.org/badge.svg)]'
             '(https://common-changelog.org)\n')

    # Comment about template
    fh.writelines([
        '<!-- Template\n',
        '## Unreleased\n',
        '### Changed\n',
        '### Added\n',
        '### Removed\n',
        '### Fixed\n',
        '-->\n'
    ])

    url = 'https://github.com/bit-team/backintime/releases/tag/v'

    # each release
    for version, date, categories in data:
        fh.write(f'\n## {version} ({date})\n')

        ref_links.append(f'[{version}]: {url}{version}\n')

        for cat in categories:
            fh.write(f'\n### {cat}\n\n')
            fh.writelines([f'- {item}\n' for item in categories[cat]])

    handle.write('\n')
    handle.writelines(ref_links)


if __name__ == '__main__':
    raw_result = main()

    result = process_raw_results(raw_result)

    # import json
    # print(json.dumps(result, indent=4))

    # suffixes = []
    # for r in result:
    #     suffixes.extend(list(r[2].keys()))

    # suffixes = sorted(set(suffixes))
    # print(suffixes)

    with Path('CHANGELOG.md').open('w', encoding='utf-8') as handle:
        to_markdown(result, handle)

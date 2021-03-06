#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2020 NXP
#
# SPDX-License-Identifier: BSD-3-Clause

"""Copyright and License Review script.

Generates a report of files that are:
- missing Copyright information
- missing NXP Copyright
- missing this year's copyright
- missing license info
- having other license than BSD-3-Clause
"""

import os
import re

from collections import namedtuple
from datetime import datetime
from typing import List, Tuple

ROOT_FOLDERS = ['spsdk', 'tests', 'examples', 'tools']
CWD = os.path.abspath(os.curdir)
ROOT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
ROOT_FOLDERS = [
    os.path.relpath(os.path.join(ROOT_DIR, path), CWD) for path in ROOT_FOLDERS
]

CLRInfo = namedtuple('CLRInfo', ['path', 'copyrights', 'license'])

COPYRIGHT_REGEX = re.compile(
    r"Copyright.*(?P<from>\d{4})?-?(?P<till>\d{4}) (?P<holder>.*)"
)
LICENSE_REGEX = re.compile(r"SPDX-License-Identifier: (?P<license>.*)")


def format_copyright_instance(copyright_instance: tuple) -> str:
    """Transform Copyright info from tuple to string.

    ('YEAR_FROM', 'YEAR_TO', 'HOLDER') -> '[YEAR_FROM-]YEAR_TO HOLDER'
    """
    from_year, to_year, holder = copyright_instance
    msg = f'{from_year}-' if from_year else ''
    msg += f'{to_year}'
    msg += f' {holder}'
    return msg


def format_copyright(copyright_info: List[Tuple[str]]) -> List[str]:
    """Transforms a list of tuples of Copyright info into a list."""
    return [
        format_copyright_instance(instance)
        for instance in copyright_info
    ]


def process_file(file_path: str) -> CLRInfo:
    """Gather copyright and license into from a file."""
    with open(file_path) as f:
        file_content = f.read()
    copyrights = COPYRIGHT_REGEX.findall(file_content)
    lic = LICENSE_REGEX.findall(file_content)
    lic = lic[0] if len(lic) > 0 else []
    return CLRInfo(file_path, format_copyright(copyrights), lic)


def get_all_files(root_folders: List[str]) -> List[str]:
    """Gather all python files in root_folders."""
    all_files = []
    for root_folder in root_folders:
        for root, _, file_names in os.walk(root_folder):
            for file_name in file_names:
                if file_name.endswith('.py'):
                    all_files.append(os.path.join(root, file_name))
    return all_files


def main() -> None:
    """Main function."""
    clr_info_list = [
        process_file(file_path)
        for file_path in get_all_files(ROOT_FOLDERS)
    ]

    print('Files without copyright info:')
    for clr_info in clr_info_list:
        if len(clr_info.copyrights) == 0:
            print(f' - {clr_info.path}')

    print('Files without "NXP" copyright:')
    for clr_info in clr_info_list:
        if not list(filter(lambda x: 'NXP' in x, clr_info.copyrights)):
            print(f' - {clr_info.path}: {clr_info.copyrights}')

    this_year = datetime.now().year
    print(f'Files without "{this_year} NXP" copyright:')
    for clr_info in clr_info_list:
        if not list(filter(lambda x: f'{this_year} NXP' in x, clr_info.copyrights)):
            print(f' - {clr_info.path}: {clr_info.copyrights}')

    print('Files without license info:')
    for clr_info in clr_info_list:
        if not clr_info.license:
            print(f' - {clr_info.path}')

    print('Files without "BSD-3-Clause" license:')
    for clr_info in clr_info_list:
        if clr_info.license != 'BSD-3-Clause':
            print(f' - {clr_info.path}: {clr_info.license}')


if __name__ == "__main__":
    main()

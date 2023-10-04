
"""
Gets the current  version.
"""

import os
import re


def get_version():
    this_dir = os.path.dirname(__file__)
    package_init_filename = os.path.join(this_dir, '../__init__.py')

    version = None
    with open(package_init_filename, 'r') as handle:
        file_content = handle.read()
        version = re.search(
            r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
            file_content, re.MULTILINE
        ).group(1)

    if not version:
        raise ValueError('Cannot find version information')

    return version

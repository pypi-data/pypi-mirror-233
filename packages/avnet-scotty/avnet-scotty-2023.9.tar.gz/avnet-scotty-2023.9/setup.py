# SPDX-FileCopyrightText: (C) 2022 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only
# noqa: D100

import setuptools
import os

_version = os.environ.get('SCOTTY_VERSION', '0.0.1')

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    author='Avnet Embedded GmbH',
    description='scotty: S(imple)C(ore) O(pen) T(echnology) T(ool for) Y(ou)',
    long_description=open('README.rst', 'r').read(),
    long_description_content_type='text/x-rst',
    license='GPL-3.0-only',
    license_files=('LICENSE',),
    entry_points={
        'console_scripts': [
            'bumper = bumper.__main__:main',
            'scotty-test = scotty_test.__main__:main',
        ],
    },
    packages=['bumper', 'scotty_test'],
    install_requires=requirements,
    include_package_data=True,
    # As scotty is already in use on PyPi our package is called
    # avnet-scotty
    name='avnet-scotty',
    scripts=[
        'scotty',
        'scotty-runqemu',
        'scripts/vm_bundle.sh',
        'scripts/vm_create.sh.template',
    ],
    url='https://github.com/avnet-embedded/simplecore-tools',
    version=_version,
)

# Copyright (C) 2018  Nexedi SA
#     Lukasz Nowak <luke@nexedi.com>
#
# This program is free software: you can Use, Study, Modify and Redistribute
# it under the terms of the GNU General Public License version 3, or (at your
# option) any later version, as published by the Free Software Foundation.
#
# You can also Link and Combine this program with other software covered by
# the terms of any of the Free Software licenses or any of the Open Source
# Initiative approved licenses and Convey the resulting work. Corresponding
# source of such a combination shall include the source code for all other
# software used.
#
# This program is distributed WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See COPYING file for full licensing terms.
# See https://www.nexedi.com/licensing for rationale and options.

from setuptools import setup, find_packages
import versioneer

tests_require = [
    'urllib3 >= 1.18',  # https://github.com/urllib3/urllib3/issues/258
    'ipaddress',
    'mock',
]

long_description = open("README.rst").read() + "\n"
long_description += open("CHANGES.rst").read() + "\n"

setup(
  name='kedifa',
  version=versioneer.get_version(),
  cmdclass=versioneer.get_cmdclass(),
  author='Lukasz Nowak',
  author_email='luke@nexedi.com',
  description="KEy DIstribution FAcility",
  long_description=long_description,
  classifiers=[
    'Environment :: Console',
    'Environment :: Web Environment',
    'Intended Audience :: System Administrators',
    'Intended Audience :: Information Technology',
    'License :: OSI Approved :: GNU General Public License v3 or '
    'later (GPLv3+)',
    'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
  ],
  keywords='key distribution ssl',
  url='https://lab.nexedi.com/nexedi/kedifa',
  license='GPLv3+ with wide exception for FOSS',
  packages=find_packages(),
  install_requires=[
    'cryptography',  # for working with certificates
    'requests',  # for getter and updater
    'zc.lockfile >= 1.4',  # for stateful updater
    'urllib3 >= 1.18',  # https://github.com/urllib3/urllib3/issues/258
    'six',  # for python 2 and 3 compatibility
    'caucase',  # provides utils for certificate management;
                # version requirement caucase >= 0.9.3 is dropped, as it
                # is not working in some cases, but fortunately KeDiFa is
                # used in places with pinned versions
  ],
  tests_require=tests_require,
  extras_require={'test': tests_require},
  zip_safe=True,
  entry_points={
    'console_scripts': [
      'kedifa = kedifa.cli:http',
      'kedifa-getter = kedifa.cli:getter',
      'kedifa-updater = kedifa.cli:updater',
    ]
  },
)

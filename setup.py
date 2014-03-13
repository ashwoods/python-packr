#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of packr.

# packr is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 2 of the
# License, or (at your option) any later version.

# packr is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with packr. If not, see
# <http://www.gnu.org/licenses/>.


from setuptools import setup

setup(name='packr',
      version='0.1.0',
      author='Carlos de las Heras',
      author_email='cahersan@gmail.com',
      url='https://github.com/cahersan/packr',
      description='Debian packaging for Django projects.',
      license='GNU General Public License v2 or later',
      scripts=['bin/packr'],
      py_modules=['packr', 'setup_parser'],
      data_files=[('templates',['templates/rules',
                                'templates/preinst',
                                'templates/changelog',
                                'templates/control'])],
      classifiers=[
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
          'Topic :: Software Development :: Build Tools',
          'Topic :: System :: Installation/Setup',
          'Topic :: Utilities',
      ])

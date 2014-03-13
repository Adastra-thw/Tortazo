# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

Tortazo.py

Tortazo is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

Tortazo is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Tortazo",
    version = "1.1",
    author = "Adastra",
    author_email = "debiadastra@gmail.com",
    description = ("Audit and Attack TOR Nodes"),
    license = "GPL",
    keywords = "stem tortazo tor",
    url = "http://packages.python.org/Tortazo",
    packages=['core', 'fuzzdb'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Audit and Hacking",
        "License :: GNU/GPL v2",
    ],
)
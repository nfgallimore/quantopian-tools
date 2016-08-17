#! /usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import os
import re
import sys

from pip.req import parse_requirements
from setuptools import setup, find_packages


def read(*names):
    with open(os.path.join(os.path.dirname(__file__), *names)) as f:
        return f.read()


special_members = {}
for line in ast.parse(read('quantopian', '__init__.py')).body:
    if (not isinstance(line, ast.Assign) or len(line.targets) != 1 or
            not isinstance(line.targets[0], ast.Name) or
            not re.match(r'__.*?__', line.targets[0].id) or
            not isinstance(line.value, ast.Str)):
        continue
    special_members[line.targets[0].id] = line.value.s

pkg_name = special_members['__pkg_name__']
py_version = sys.version_info[0]

setup(
    name=pkg_name,
    version=special_members.get('__version__'),
    description=special_members.get('__project_description__'),
    long_description=read('README.md') + '\n\n\n' + read('LICENSE'),
    author=special_members.get('__author__'),
    author_email=special_members.get('__author_email__'),
    maintainer=special_members.get('__maintainer__'),
    maintainer_email=special_members.get('__maintainer_email__'),
    url=special_members.get('__project_url__'),
    packages=find_packages(exclude=['tests']),
    license=special_members.get('__license__'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=[str(x.req) for x in parse_requirements('requirements/install-py%d.txt' % py_version,
                                                             session=False)],
    tests_require=[str(x.req) for x in parse_requirements('requirements/py%d.txt' % py_version, session=False)],
    include_package_data=True,
    zip_safe=False
)

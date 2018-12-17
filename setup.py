#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='pyAndorNeo',
      version='2018',
      description='Andor Neo drivers in Python using SDK3',
      long_description=readme(),
      url='https://github.com/scivision/pyAndorNeo',
      author='David Baddeley',
      author_email='d.baddeley@auckland.ac.nz',
      license='GPLv3',
      packages=['AndorNeo'],
      install_requires=[])

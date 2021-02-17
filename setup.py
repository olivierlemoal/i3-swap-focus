#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name='i3-swap-focus',
    version='0.2',
    description='i3 script to toggle between last windows',
    packages=find_packages(),
    author='Olivier Le Moal',
    author_email='mail@olivierlemoal.fr',
    url='https://github.com/olivierlemoal/i3-swap-focus',
    license='MIT',
    platforms=['any'],
    install_requires=['i3ipc'],
    scripts=['i3_swap_focus'],
)

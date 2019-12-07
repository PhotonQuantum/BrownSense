#!/usr/bin/env python3

from setuptools import setup

import PiPyADC


setup(
    name='PiPyADC',
    version=PiPyADC.version,
    description="Python module for interfacing Texas Instruments SPI bus based analog- to-digital converters with the Raspberry Pi.",
    author='ul-gh',
    packages=[
        'PiPyADC',
    ],
    url='https://github.com/ul-gh/PiPyADC',
    classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)'
    ],
    install_requires=[
        'wiringpi',
    ]
)

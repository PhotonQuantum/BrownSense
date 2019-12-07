#!/usr/bin/env python3

from setuptools import setup

import BrownSense


setup(
    name='BrownSense',
    version=BrownSense.__version__,
    description="A distributed IoT platform for monitoring and improving toilet's indoor air quality.",
    author='LightQuantum',
    author_email='cy.n01@outlook.com',
    packages=[
        'BrownSense',
    ],
    url='https://github.com/PhotonQuantum/BrownSense',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    install_requires=[
        'cloudant',
        'requests',
        'loguru',
        'PiPyADC'
    ],
    entry_points={
        'console_scripts': [
            "brownsense=BrownSense.main:main",
        ]
    },
    python_requires='>=3.6'
)

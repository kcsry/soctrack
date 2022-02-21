#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='soctrack',
    version='0.2',
    description='Social Media Tracker',
    author='Aarni Koskela',
    author_email='akx@desucon.fi',
    url='https://github.com/kcsry/soctrack',
    packages=find_packages('.', include=('soctrack', 'soctrack.*')),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Django>=3.0', 'requests', 'jsonfield'],
)

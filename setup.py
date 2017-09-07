#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'numpy'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pybreach',
    version='0.3.0',
    description="Identification of temporal consistency in rating curve data: Bidirectional Reach (BReach)",
    long_description=readme + '\n\n' + history,
    author="Stijn Van Hoey",
    author_email='stijnvanhoey@gmail.com',
    url='https://github.com/stijnvanhoey/pybreach',
    packages=[
        'pybreach',
    ],
    package_dir={'pybreach':
                 'pybreach'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pybreach',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)

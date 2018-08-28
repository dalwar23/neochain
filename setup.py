#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup script for neochain
Install neochain with
python setup.py install
"""

# Source code meta data
__author__ = 'Dalwar Hossain'
__email__ = 'dalwar.hossain@protonmail.com'

# Import python libraries
import os
import sys
from setuptools import setup


# Check if enough parameter has been given to install or not
if sys.argv[-1] == 'setup.py':
    print("To install, run 'python setup.py install'")
    print()


# Check python version before installing
if sys.version_info[:2] < (2, 7):
    print("NEOChain requires Python 2.7 or later (%d.%d detected)." % sys.version_info[:2])
    sys.exit(-1)


# Get version and release for this package
package_name = 'neochain'
release_file = os.path.join(package_name, '_release_info.py')
release_info = {}
with open(release_file, 'rb') as rf:
    exec(rf.read(), release_info)


# Read the README.md file for long description
def readme():
    with open('README.rst') as f:
        return f.read()


# Standard boilerplate to run this script
if __name__ == "__main__":
    setup(
        name=package_name,
        version=release_info['__version__'],
        maintainer='Dalwar Hossain',
        maintainer_email='dalwar.hossain@protonmail.com',
        author=release_info['__author__'],
        author_email=release_info['__email__'],
        description='neochain - Network Evolution Observation for Blockchain',
        keywords=['Network', 'Evolution', 'Community', 'Blockchain'],
        long_description=readme(),
        license='MIT',
        platforms=['Linux', 'Mac OSX', 'Windows', 'Unix'],
        url='https://github.com/dharif23/neochain',
        download_url='https://github.com/dharif23/neochain',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Topic :: Software Development :: Libraries :: Python Modules'],
        packages=['neochain'],
        include_package_data=True,
        install_requires=['pip>=18.0',
                          'numpy!=1.15.0',
                          'pandas>=0.23.4',
                          'networkx>=2.1',
                          'python-louvain>=0.11',
                          'pyrainbowterm>=1.0',
                          'setuptools>=40.1.0',
                          'six>=1.10.0',
                          'wheel>=0.31.1',
                          'python-dateutil>=2.7.3',
                          'pytz>=2018.5',
                          'sphinx>=1.7.1',
                          'recommonmark >=0.4.0',
                          'sphinx_rtd_theme>=0.4.1',
                          ],
        test_suite='nose.collector',
        tests_require=['nose>=1.3.7', 'nose-cover3>=0.1.0'],
        zip_safe=False,
    )

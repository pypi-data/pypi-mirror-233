#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
from setuptools import find_packages, setup


if sys.version_info < (3, 9, 0, 'final', 0):
    raise SystemExit('Python 3.9 or later is required!')

# Fetch information available in module
with open('README.rst', encoding='utf-8') as fd:
    long_description = fd.read()

with open('mumott/__init__.py', encoding='utf-8') as fd:
    lines = '\n'.join(fd.readlines())

version = re.search("__version__ = '(.*)'", lines).group(1)
description = re.search("__description__ = '(.*)'", lines).group(1)
maintainer = re.search("__maintainer__ = '(.*)'", lines).group(1)
url = re.search("__url__ = '(.*)'", lines).group(1)
license = re.search("__license__ = '(.*)'", lines).group(1)

# Set classifiers used on PyPI
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: {}'.format(license),
    'Topic :: Scientific/Engineering :: Chemistry',
    'Topic :: Scientific/Engineering :: Image Processing',
    'Topic :: Scientific/Engineering :: Physics',
    'Topic :: Scientific/Engineering :: Visualization']

# Python libraries this package depends on
python_dependencies = ['colorcet',
                       'colorspacious',
                       'matplotlib',
                       'h5py',
                       'numba<=0.56.3',
                       'numpy>=1.20.0,<=1.24.0',
                       'scipy',
                       'scikit-image',
                       'tqdm']

# Carry out the actual package installation and setup
setup(name='mumott',
      py_modules=['mumott'],
      version=version,
      description=description,
      long_description=long_description,
      maintainer=maintainer,
      url=url,
      license=license,
      classifiers=classifiers,
      install_requires=python_dependencies,
      packages=find_packages(),
      zip_safe=False,
      package_data={'': ['core/*.h5']},
      include_package_data=True)

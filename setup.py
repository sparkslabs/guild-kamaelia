#!/usr/bin/python
#

from distutils.core import setup
from distutils.version import LooseVersion
import os

def is_package(path):
    return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, '__init__.py'))
        )

def find_packages(path, base="" ):
    """ Find all packages in path """
    packages = {}
    for item in os.listdir(path):
        dir = os.path.join(path, item)
        if os.path.isdir(dir):
            if base:
                module_name = "%(base)s.%(item)s" % vars()
            else:
                module_name = item
            if is_package( dir ):
                packages[module_name] = dir
            packages.update(find_packages(dir, module_name))
    return packages


packages = find_packages(".")
package_names = packages.keys()

setup(name = "guild-kamaelia",
      version = "0.0.1",
      description = "Kamaelia partial-compatibility layer for guild",
      url='http://www.sparkslabs.com/michael/',
      author='Michael Sparks',
      author_email='michael.sparks@rd.bbc.co.uk',
      license='Apache Software License',

      packages = package_names,
      package_dir = packages,
      package_data={'': ['templates/*']},
      long_description = """
Kamaelia partial-compatibility layer for guild
"""
      )

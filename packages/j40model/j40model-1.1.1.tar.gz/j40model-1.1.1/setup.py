# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='j40model',
    version='1.1.1',
    description='Base simulation and optimization modules for J40 tool',
    long_description=readme,
    url='https://github.com/LBNLgrid/j40model',
    author='Miguel Heleno',
    author_email='miguelhelenoa@lbl.gov',
    include_package_data=True,
    install_requires=['geopandas',
                      'numpy',
                      'pandas',
                      'Pyomo']
)

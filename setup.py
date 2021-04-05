# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in renovation_core_graphql/__init__.py
from renovation_core_graphql import __version__ as version

setup(
	name='renovation_core_graphql',
	version=version,
	description='GraphQL Wrapper for renovation_core',
	author='Leam Technology Systems',
	author_email='info@leam.ae',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

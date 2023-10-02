import setuptools
from setuptools import setup

setup(
	name='techdocs',
	version='0.1.2',
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'techdocs=techdocs.cli:main'
        ]
    },

    # data_files=[('techdocs', ['techdocs/utils/*.json'])],

    packages=setuptools.find_packages(),
)
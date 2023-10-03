from setuptools import setup, find_packages

setup(
    name='waveboxgen',
    version='0.1-dev',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'waveboxgen = waveboxgen.main:main'
        ]
    }
)
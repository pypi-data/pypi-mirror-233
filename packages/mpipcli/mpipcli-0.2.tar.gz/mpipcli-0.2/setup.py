
from setuptools import setup

VERSION = '0.2'

setup(
    name='mpipcli',
    version=VERSION,
    packages=['mpip'],
    entry_points={
        'console_scripts': [
            'mpip = mpip.cli:main',
        ],
    },
    install_requires=[
        'requests'
    ],
)









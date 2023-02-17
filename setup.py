#!/usr/bin/env python3

from setuptools import setup

with open('version', 'r') as file:
    version = file.readline().replace('\n', '')

setup(
    name='bbg_telegram_media_server',
    version=version,
    python_requires='>3.5',
    package_dir={'bbg_telegram_media_server': 'src/bbg_telegram_media_server'},
    packages=['bbg_telegram_media_server'],
    install_requires=['python-telegram-bot'],
    entry_points={
        'console_scripts': [
            'bbg-telegram-media-server = bbg_telegram_media_server.bbg_telegram_media_server:main',
        ]
    }
)

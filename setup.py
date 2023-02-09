from setuptools import setup

setup(
    name='bbg_telegram_media_server',
    version='0.0.1',
    package_dir={'bbg_telegram_media_server': 'src/bbg_telegram_media_server'},
    packages=['bbg_telegram_media_server'],
    install_requires=[
        'libtorrent', 'python-telegram-bot'
    ],
    entry_points={
        'console_scripts': [
            'bbg-telegram-media-server = bbg_telegram_media_server.bbg_telegram_media_server:main',
        ]
    }
)

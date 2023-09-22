from setuptools import setup, find_packages

with open("version", "r") as f:
    version = f.read().strip()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="bbg-telegram-media-server",
    version=version,
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "bbg-telegram-media-server=bbg_telegram_media_server.bbg_telegram_media_server:main"
        ],
    },
)

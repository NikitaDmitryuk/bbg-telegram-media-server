from setuptools import setup, Extension
from Cython.Build import cythonize
from Cython.Compiler import Options

import os

os.environ['LDSHARED'] = 'arm-cortexa8_neon-linux-gnueabihf-gcc -shared'

Options.embed = 'main'

extensions = [Extension("src/*", ["src/*.py"],
                        include_dirs=['/usr/include', '/usr/include/arm-linux-gnueabihf'])]

setup(
    name="bbg-telegram-media-server",
    ext_modules=cythonize(extensions, language_level="3")
)

CC=arm-cortexa8_neon-linux-gnueabihf-gcc
CYTHON=cython
PYTHON := python3
PYVERSION := $(shell $(PYTHON) -c "import platform; print('.'.join(platform.python_version_tuple()[:2]))")
PYPREFIX := $(shell $(PYTHON) -c "import sys; print(sys.prefix)")
INCDIR := $(shell $(PYTHON) -c "from distutils import sysconfig; print(sysconfig.get_python_inc())")
INCLUDES=-I$(PYPREFIX)/include/python$(PYVERSION) -I/usr/include -I/usr/include/arm-linux-gnueabihf -I$(INCDIR)
FILES_TO_BUILD := $(shell find "${PWD}" -maxdepth 1 -name '*.py' -printf "%f\n" | sed -r "s/(.*).py/\1.o/g")

.PHONY: all

all: bbg-telegram-media-server

bbg-telegram-media-server: $(FILES_TO_BUILD)
	$(CC) -o $@ $^ -pthread -fPIC -fwrapv -O3 -Wall -fno-strict-aliasing -L /usr/lib/python$(PYVERSION)/config-$(PYVERSION)-arm-linux-gnueabihf -L /usr/lib/arm-linux-gnueabihf -L /lib/arm-linux-gnueabihf -lpython$(PYVERSION) -lexpat -lz -lm
%.o: %.c
	$(CC) -c -o $@ $< $(INCLUDES)

%.c: %.py
	$(CYTHON) $<

bbg_telegram_media_server.c: bbg_telegram_media_server.py
	$(CYTHON) --embed $<

FROM ubuntu
RUN apt-get update
RUN apt-get install -y python3-pip python3-libtorrent
RUN pip install pyinstaller python-telegram-bot

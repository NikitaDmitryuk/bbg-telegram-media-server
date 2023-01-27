FROM ubuntu

ENV WDIR /workdir

RUN apt-get update
RUN apt-get install -y python3-pip python3-libtorrent
RUN pip install pyinstaller python-telegram-bot

VOLUME $WDIR
WORKDIR $WDIR

# COPY entrypoint.sh /
# ENTRYPOINT ["/entrypoint.sh"]

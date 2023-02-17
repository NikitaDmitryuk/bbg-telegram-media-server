#!/usr/bin/env bash

docker run --rm dockcross/linux-armv7a-lts > ./dockcross-linux-armv7a-lts && chmod +x ./dockcross-linux-armv7a-lts

./dockcross-linux-armv7a-lts ./entrypoint.sh

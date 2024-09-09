#!/usr/bin/env bash

set -e
set -x

poetry run mypy --disallow-untyped-defs --follow-imports=skip bbg_telegram_media_server
poetry run flake8 bbg_telegram_media_server

poetry run black --check --diff bbg_telegram_media_server
poetry run isort --check-only bbg_telegram_media_server

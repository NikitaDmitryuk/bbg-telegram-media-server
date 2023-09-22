.PHONY: lint format setup_env test_debug build

lint:
	.githooks/lint.sh

format:
	poetry run isort --force-single-line-imports bbg_telegram_media_server
	poetry run autoflake --recursive --remove-all-unused-imports --ignore-init-module-imports --in-place bbg_telegram_media_server
	poetry run black bbg_telegram_media_server
	poetry run isort bbg_telegram_media_server

setup_env:
	poetry config virtualenvs.create true
	poetry config virtualenvs.in-project true
	poetry install

debug:
	PYTHONDONTWRITEBYTECODE=1 poetry run python bbg-telegram-media-server.py

build:
	./build.sh

clear:
	find . -depth -type d -name "__pycache__" -exec rm -r {} \;

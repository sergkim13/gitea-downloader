install:
	poetry install

start:
	poetry run python -m main

test:
	poetry run pytest -vv

test-cov:
	poetry run pytest --cov-report term-missing --cov=gitea_downloader --cov-report xml
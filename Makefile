install:
	poetry install

start:
	poetry run python main.py

test:
	poetry run pytest -vv

lint:
	poetry run flake8 gitea_downloader

test-cov:
	poetry run pytest --cov-report term-missing --cov=gitea_downloader --cov-report xml

.PHONY: lint format

lint:
    poetry run flake8 .

format:
    poetry run black .
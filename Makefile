all: lint

.PHONY: lint
lint:
	flake8 --ignore=E501
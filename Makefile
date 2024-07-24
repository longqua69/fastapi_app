.PHONY: lint pylint mypy format isort black

lint: pylint mypy
format: isort black

pylint:
	pylint src/

mypy:
	mypy src/

black:
	black src/

isort:
	isort src/
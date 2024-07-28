.PHONY: lint pylint mypy format isort black check-isort check-black

lint: pylint mypy
format: isort black
check-formatting: check-isort check-black

pylint:
	pylint src/

mypy:
	mypy src/

black:
	black src/

isort:
	isort src/

check-isort:
	isort --check src/

check-black:
	black --check src/

.PHONY: help init clean test validate mock create delete info deploy
.DEFAULT_GOAL := help
environment = "inlined"
init: ## init python
		@pipenv install --python /usr/bin/python3 --dev
test: ## run the unit tests v2
		@pipenv run python -m pytest -x --cov=src
		@pipenv run coverage report -m
		@pipenv run coverage xml
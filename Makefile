.PHONY: initial_setup venv_config run

initial_setup:
	pipenv --python 3.9

venv_config: initial_setup
	(pipenv sync;pipenv shell)

run:
	python main/main.py -i $(filename)
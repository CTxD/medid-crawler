test:
	pytest -v --cov=source tests/ --cov-report term --cov-report html --show-capture=no

install:
	python3 install.py

main:
	python3 main.py
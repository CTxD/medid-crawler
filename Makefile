test:
	pytest -v --cov=source tests/

install:
	python install.py

main:
	python main.py
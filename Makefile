install:
	pip install projen

synth:
	projen --post false

update-deps:
	poetry update
install:
	pip install projen

synth:
	projen --post false

update-deps:
	poetry update

docker-start:
	sudo systemctl start docker

cdk-deploy-all:
	cdk deploy --all --require-approval never --app "python app.py" --profile dev
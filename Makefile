-include .env
export

PYTHON_VERSION=3.10.11

python-setup:
	pyenv install --skip-existing $(PYTHON_VERSION)
	pyenv local $(PYTHON_VERSION)

openai-mock:
	docker run -d --name openai -p 8080:8080 -v $$(pwd):/tmp -e "OPENAPI_MOCK_SPECIFICATION_URL=/tmp/openapi-openai-mock.yaml" muonsoft/openapi-mock

db-setup:
	docker run -d --name mongo -p 27017:27017 mongo

setup: db-setup python-setup

reqs:
	. .venv/bin/activate
	pip install -r requirements.txt
	@echo "==================="
	@echo "Virtual environment successfully created. To activate the venv:"
	@echo "	\033[0;32msource .venv/bin/activate"

venv:
	pyenv exec python -m venv .venv
	make reqs

api-dev:
	uvicorn api.entry:app --host 0.0.0.0 --port 8000 --reload
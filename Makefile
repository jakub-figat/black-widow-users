format:
	docker-compose run --rm app bash -c "isort . && black ."

check:
	docker-compose run --rm app bash -c "prospector ."

build:
	docker-compose build

run:
	docker-compose up

deploy:
	docker-compose run --rm app bash -c "chalice deploy"

bash:
	docker-compose run --rm app bash

unit-test:
	docker-compose run --rm app bash -c "coverage run --source=chalicelib -m pytest tests/unit/"

integration-test:
	docker-compose run --rm app bash -c "coverage run --source=chalicelib -m pytest tests/integration/"

test:
	docker-compose run --rm app bash -c "coverage run --source=chalicelib -m pytest tests/"

cov-report:
	docker-compose run --rm app bash -c "coverage report"

cov-html:
	docker-compose run --rm app bash -c "coverage html"
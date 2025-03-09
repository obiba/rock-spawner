env_path=.env

build:
	poetry build

install:
	poetry install

update:
	poetry lock

#test:
#	poetry run pytest -s

shell:
	poetry shell

run:
	poetry run dotenv -f "$(env_path)" run uvicorn rock_spawner.main:app --reload --port 8086

#lint:
#	poetry run pre-commit run --all-files

docker-build:
	docker build --no-cache=true -t obiba/rock-spawner:snapshot .
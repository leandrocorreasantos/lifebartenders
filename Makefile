DOCKER_CMD=docker exec -it lifebartenders

_config-env:
	[ -f .env ] || cp .env.sample .env

flake8:
	${DOCKER_CMD} flake8 --exclude=templates,static,venv,tests,migrations

build: _config-env
	docker-compose up -d

stop:
	docker-compose stop

upgrade-pip:
	${DOCKER_CMD} pip install --upgrade pip

setup: upgrade-pip
	${DOCKER_CMD} pip install -r requirements.txt

start:
	${DOCKER_CMD} python app.py

migrate-init:
	${DOCKER_CMD} flask db init

migrate:
	${DOCKER_CMD} flask db migrate

migrate-apply:
	${DOCKER_CMD} flask db upgrade

migrate-rollback:
	${DOCKER_CMD} flask db downgrade -1

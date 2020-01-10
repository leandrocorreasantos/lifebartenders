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
	${DOCKER_CMD} python lifebartenders/app.py

migrate-init:
	${DOCKER_CMD} python lifebartenders/manager.py db init

migrate:
	${DOCKER_CMD} python lifebartenders/manager.py db migrate

migrate-apply:
	${DOCKER_CMD} python lifebartenders/manager.py db upgrade

migrate-rollback:
	${DOCKER_CMD} python lifebartenders/manager.py db downgrade -1

seed:
	${DOCKER_CMD} python lifebartenders/manager.py seed

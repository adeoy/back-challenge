install-local:
	python3 -m pip install --upgrade pip pipenv
	pipenv --three
	pipenv install

remove-unused:
	@echo "Remove unused..."
	autoflake --recursive --in-place --remove-all-unused-imports --remove-unused-variables ./

sort:
	@echo "Sorting..."
	isort .

format:
	@echo "Blacking..."
	black .

lint-fix: sort remove-unused format sort

requirements:
	@echo "Creating requirements.txt..."
	pipenv lock -r --dev > requirements.txt

pip-lock:
	@echo "Pipenv Lock..."
	pipenv lock

check-env:
	@if [ ! -f .env ]; then cp .env.dist .env; fi

up: check-env
	@docker-compose -f infrastructure/docker-compose.yml up --build;

tests: check-env
	@docker-compose -f infrastructure/docker-compose.yml run --rm api python manage.py test api/tests

coverage: check-env
	@echo "Make Coverage"
	@docker-compose -f infrastructure/docker-compose.yml run --rm api coverage run --source='.' manage.py test api/tests

coverage-report: coverage
	@echo "Make Coverage Report"
	@docker-compose -f infrastructure/docker-compose.yml run --rm api coverage report

migrations: check-env
	@echo "Django. Make Migrations"
	@docker-compose -f infrastructure/docker-compose.yml run --rm api python manage.py makemigrations

migrate: migrations
	@echo "Django. Migrate"
	@docker-compose -f infrastructure/docker-compose.yml run --rm api python manage.py migrate

install: migrate up

stop:
	@echo "Stopping containers..."
	@docker stop back-challenge-api back-challenge-proxy

remove: stop
	@echo "Removing containers..."
	@docker rm back-challenge-api back-challenge-proxy

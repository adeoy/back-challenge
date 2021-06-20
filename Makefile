install-local:
	python3 -m pip install --upgrade pip pipenv
	pipenv --three
	pipenv install

check-env:
	@if [ ! -f .env ]; then cp .env.dist .env; fi

lint-fix: check-env
	@echo "Formatting..."
	@docker-compose -f infrastructure/docker-compose.yml run --rm api isort . && autoflake --recursive --in-place --remove-all-unused-imports --remove-unused-variables ./ && black . && isort .

requirements: check-env
	@echo "Creating requirements.txt..."
	@docker-compose -f infrastructure/docker-compose.yml run --rm api pipenv lock -r --dev > requirements.txt

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

create-superuser: check-env
	@echo "Django. Create superuser"
	@docker-compose -f infrastructure/docker-compose.yml run --rm api python manage.py createsuperuser

db-populate:
	docker exec back-challenge-db /bin/sh -c 'mysql -u root -p12345678 </tmp/back_challenge.sql'

stop-containers: check-env
	@echo "Stopping containers..."
	@docker stop back-challenge-api back-challenge-proxy

remove-containers: stop-containers
	@echo "Removing containers..."
	@docker rm back-challenge-api back-challenge-proxy

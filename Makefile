install:
	pip3 install pipenv
	pipenv --three
	pipenv install

remove-unused:
	@echo "Remove unused..."
	autoflake --recursive --in-place --remove-all-unused-imports --remove-unused-variables ./

sort:
	@echo "Sorting..."
	isort api/
	isort app/

format:
	@echo "Blacking..."
	black api/
	black app/

lint-fix: sort remove-unused format sort

requirements:
	@echo "Creating requirements.txt..."
	pipenv run pip freeze > requirements.txt

start:
	@echo "Run Local in Debug..."
	python migrate.py runserver

pip-lock:
	@echo "Pipenv Lock..."
	pipenv lock

up:
	@if [ ! -f .env ]; then cp .env.example .env; fi
	@docker-compose -f infrastructure/docker-compose.yml up --build;
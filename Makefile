default: format

# Styling commands
format:
	echo "Formatting code"
	black rest_api
	isort rest_api --profile black
	echo "Formatted successfully"

lint:
	echo "Linting app directory"
	flake8 rest_api/
	echo "Linted successfully"

# Local development commands
run-backend:
	echo "Running backend"
	python manage.py check_db
	python manage.py check_or_create_user
	python manage.py runserver

tests:
	echo "Running tests for rest_api"
	python manage.py test

# Database commands
migrations:
	echo "Making app migrations"
	python manage.py makemigrations rest_api
	echo "Making app migrate"
	python manage.py migrate rest_api

checkmigrations:
	python manage.py makemigrations --check --no-input --dry-run

# Docker commands
docker-build:
	docker-compose -f deployment/local/docker-compose.yml up --build
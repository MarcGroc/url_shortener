# URL shortener
 ### A simple URL shortener with IP and click tracking.
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)


## Introduction

This is a simple URL shortener written with:
- Python
- Django
- Django REST Framework
- Docker
- PostgreSQL
- Celery
- Redis

## Documentation

- Detailed documentation can be found in the [docs](docs) directory.

## Installation

1. Clone the repository
```bash
git clone https://github.com/MarcGroc/url_shortener.git
```
2. cd into the project directory
```bash
cd url_shortener
```
3. Create a `.env` file in the `deployment/local/` of the project and add the following environment variables:
``` bash
#Debug
DEBUG=True

#Allowed hosts for cors
ALLOWED_HOSTS=*

# Database credentials
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=url_shortener
DB_HOST=db
DB_PORT=5432

#Secret key
SECRET_KEY=change_me

#Celery settings
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=django-db

#Susperuser credentials
SUPERUSER_USERNAME=change_me
SUPERUSER_PASSWORD=change_me
SUPERUSER_EMAIL=q@q.com
```
3.1 If you have Make installed, run the following command:
```bash
make docker-build
```
3.2 If you don't have Make installed, run the following commands:
```bash
cd deployment/local
docker-compose up --build
```


## Usage

1. Go to `http://localhost:8000/create`
2. Enter a URL in the input field
3. Click the "POST" button 
4. Click or copy the shortened URL 
5. Paste the shortened URL in your browser
6. You will be redirected to the original URL
7. You can access all your shortened URLs at `http://localhost:8000/my-urls/`
8. You can also access the admin panel at `http://localhost:8000/admin/` with the credentials you set in the `.env` file
9. You can also access th OpenAPI docs at `http://localhost:8000/docs/`
# URL shortener

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)


## Introduction

This is a simple URL shortener written in Python, Django, Django REST Framework, and PostgreSQL.

## Documentation

- Detailed documentation can be found in the [docs](docs) directory.

## Installation

1. Clone the repository
2. Run docker-compose up

``` bash
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=your_database_port
```


## Usage

1. Go to `http://localhost:8000/`
2. Enter a URL in the input field
3. Customize the shortened URL (optional)
4. Click the "Shorten" button
5. Copy the shortened URL 
6. Paste the shortened URL in your browser
7. Enjoy!


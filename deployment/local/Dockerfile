FROM python:3.10

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install --upgrade pip && pip install poetry

COPY ../../pyproject.toml /app/
COPY ../../poetry.lock /app/

RUN poetry config virtualenvs.create true
RUN poetry install --no-dev --no-root --no-interaction --no-ansi


COPY . /app/


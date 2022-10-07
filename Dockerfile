FROM python:3.10-slim-buster

ARG POETRY_VERSION=1.2.1

ENV PYTHONUNBUFFERED=1

RUN pip install "poetry==$POETRY_VERSION" && poetry config virtualenvs.create false

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

COPY . /app
RUN ["poetry", "install", "--no-interaction", "--no-ansi"]

ENTRYPOINT [ "python", "-m", "mantra" ]


############
# Base Image
############
FROM python:3.7-alpine3.18 AS base

WORKDIR /app

RUN apk add --no-cache -q \
    bash \
    gcc \
    libc-dev \
    libffi-dev

COPY . ./

RUN pip install tox twine

ARG PYPI_PASSWORD
ARG PYPI_USERNAME

RUN python setup.py sdist

###############
# Publish Image
###############
FROM base as publish

RUN twine --version \
 && twine upload dist/*

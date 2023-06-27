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

ENV REPO_NAME="pypi.pdg.io"
ENV REPO_URL="https://pypi.pdg.io/"
ENV PYPI_USERNAME=$PYPI_USERNAME
ENV PYPI_PASSWORD=$PYPI_PASSWORD

RUN python setup.py sdist

################
# Publish Image
################
FROM base as publish

RUN twine --version \
 && twine upload dist/*

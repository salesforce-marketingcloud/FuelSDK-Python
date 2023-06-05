############
# Base Image
############
FROM python:3.11.3-alpine as base

WORKDIR /app

RUN apk add --no-cache --no-progress \
        bash \
        build-base \
        curl

COPY . .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


################
# Publish Image
################
FROM base as publish

ARG PYPI_USERNAME
ARG PYPI_PASSWORD

RUN python publish.py

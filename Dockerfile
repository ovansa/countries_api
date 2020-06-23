# Look for available docker images from Docker hub
FROM python:3.7-alpine
MAINTAINER Muhammed Ibrahim

ENV PYTHONUNBUFFERED 1

# Copy the requirement.txt file
COPY ./requirements.txt /requirements.txt

# Install postgresql client using package manager for alpine
RUN apk add --update --no-cache postgresql-client

# Install temporary requirements
RUN apk add --update --no-cache --virtual .temp-build-deps \
      gcc libc-dev linux-headers postgresql-dev

# Install dependencies
RUN pip install -r /requirements.txt

# Delete temporary requirements
RUN apk del .temp-build-deps

# Create an empty folder in the docker image
RUN mkdir /app

# Switches as default directory
WORKDIR /app

# Copy app folder from local folder to docker image
COPY ./app /app

# Create a user that'll run application using Docker
RUN adduser -D user
USER user

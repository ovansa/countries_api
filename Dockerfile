# Look for available docker images from Docker hub
FROM python:3.7-alpine
MAINTAINER Muhammed Ibrahim

ENV PYTHONUNBUFFERED 1

# Copy the requirement.txt file
COPY ./requirements.txt /requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Create an empty folder in the docker image
RUN mkdir /app

# Switches as default directory
WORKDIR /app

# Copy app folder from local folder to docker image
COPY ./app /app

# Create a user that'll run application using Docker
RUN adduser -D user
USER user

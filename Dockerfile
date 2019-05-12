FROM python:3.7-alpine

MAINTAINER LUCI

# No buffering of outputs
ENV PYTHONUNBUFFERED 1


# Requirements
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# make the app directory and change the working directory to it.
RUN mkdir /app
WORKDIR /app
COPY ./app /app


# Create a new user
RUN adduser -D luci
USER luci


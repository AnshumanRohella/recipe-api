FROM python:3.7-alpine

MAINTAINER LUCI

# No buffering of outputs
ENV PYTHONUNBUFFERED 1


# Requirements
COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

# make the app directory and change the working directory to it.
RUN mkdir /app
WORKDIR /app
COPY ./app /app


# Create a new user
RUN adduser -D luci
USER luci


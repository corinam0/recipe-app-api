FROM python:3.7-alpine
LABEL maintainer=corinam0

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt/ /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# Created a separate user just for the application for security purposes
RUN adduser -D user
USER user

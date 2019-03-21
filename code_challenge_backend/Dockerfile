FROM python:latest
ENV PYTHONUNBUFFERED 1

ARG requirements=requirements/production.txt
ENV DJANGO_SETTINGS_MODULE=code_challenge_backend.settings.production

RUN mkdir /project
WORKDIR /project
# Installing OS Dependencies
RUN apt-get update && apt-get upgrade -y 
RUN apt-get install -y gdal-bin netcat
RUN pip install -U pip setuptools

COPY requirements/ /project/requirements/

RUN pip install -r $requirements


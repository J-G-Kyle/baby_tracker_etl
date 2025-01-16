FROM python:3.11
FROM apache/superset:4.1.1rc1-py311

USER root

# Install dependencies
COPY requirements.txt /app
WORKDIR /app
RUN pip3 install -r requirements.txt

# set pythonpath environment variable
ENV PYTHONPATH="${PYTHONPATH}:/app"

# WORKDIR /app

COPY . /app
#COPY --chown=superset data .
#COPY --chown=superset assets .

#TODO work out how to give superset user the right permissions to modify files
USER root
USER superset

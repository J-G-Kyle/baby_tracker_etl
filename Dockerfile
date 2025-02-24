FROM python:3.11
FROM sitespeedio/node:ubuntu-22.04-nodejs-18.16.0

# Install required utilities
RUN apt-get update && apt-get install -y \
    curl wget nano git xdg-utils make npm pip && \
    npm install -g degit && \
    mkdir -p /evidence-bin && \
    rm -rf /var/lib/apt/lists/*

# Create directory for staging and clean data
RUN mkdir -p /baby_tracker_etl/pipeline/data/staging
RUN mkdir -p /baby_tracker_etl/pipeline/data/clean

# create user and give permission to write and delete from the required directory
RUN useradd -ms /bin/bash dockeruser
RUN chown -R dockeruser:dockeruser /baby_tracker_etl/pipeline/data
USER dockeruser

# Install dependencies
COPY requirements.txt /baby_tracker_etl/
WORKDIR /baby_tracker_etl/
RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8

COPY config ./config
COPY pipeline ./pipeline
COPY Makefile .

WORKDIR /evidence

ENTRYPOINT [ "bash", "/evidence/bootstrap.sh" ]

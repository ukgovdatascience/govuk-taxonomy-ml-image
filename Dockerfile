FROM python:3.6.2

MAINTAINER Matthew Upson
LABEL date="2017-11-25"
LABEL version="0.1.1"
LABEL description="Image for running TPOT for automated tagging of GOV.UK content"

# Update server and install git 

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y git

COPY ./src src

# Set working directory

WORKDIR /src

# Install python requirements

RUN pip install -r requirements.txt

# Set environment variables

ENV TESTSIZE 0.2
ENV CV 5
ENV GENERATIONS 1
ENV POPULATIONSIZE 10
ENV RANDOMSTATE 1337
ENV DOCKERDATADIR /mnt/data

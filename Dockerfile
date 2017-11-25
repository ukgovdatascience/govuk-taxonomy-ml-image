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

ENV DOCKERDATADIR /mnt/data

ENV TPOT_MEMORY /mnt/data
ENV TPOT_VERBOSITY 3
ENV TPOT_NUMJOBS -1
ENV TPOT_TESTSIZE 0.2
ENV TPOT_CV 5
ENV TPOT_GENERATIONS 1
ENV TPOT_POPULATIONSIZE 10
ENV TPOT_RANDOMSTATE 1337


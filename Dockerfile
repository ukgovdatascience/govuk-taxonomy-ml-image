FROM python:3.4.6

MAINTAINER Matthew Upson
LABEL date="2017-11-22"
LABEL version="0.1.0"
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

#ENV DATADIR /mnt/data/
#ENV LOGGING_CONFIG /mnt/output

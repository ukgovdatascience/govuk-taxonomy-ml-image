#!/bin/bash
ENV=./.env-remote

docker run -i --rm \
    --env-file $ENV \
    -v $DATADIR:/mnt/DATA \
    ukgovdatascience/govuk-word-embedding:latest python TPOT_allgovuk.py

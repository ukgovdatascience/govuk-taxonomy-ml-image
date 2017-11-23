#!/bin/bash
ENV=./.env

docker run -i --rm \
    --env-file $ENV \
    -v $DATADIR:/mnt/data \
    ukgovdatascience/govuk-taxonomy-ml-image:latest python TPOT_allgovuk.py

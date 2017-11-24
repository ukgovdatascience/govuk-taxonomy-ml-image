#!/bin/bash
#ENV=./.env

#docker run -i --rm \
#    --env-file $ENV \
#    -v $LOCALDATADIR:$DOCKERDATADIR \
#    ukgovdatascience/govuk-taxonomy-ml-image:latest python TPOT_allgovuk.py

docker run -i --rm \
    -v /data:/mnt/data \
    ukgovdatascience/govuk-taxonomy-ml-image:latest python TPOT_allgovuk.py

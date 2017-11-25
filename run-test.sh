#!/bin/bash
#ENV=./.env

#docker run -i --rm \
#    --env-file $ENV \
#    -v $LOCALDATADIR:$DOCKERDATADIR \
#    ukgovdatascience/govuk-taxonomy-ml-image:latest python TPOT_allgovuk.py

docker run -i --rm \
    -v /data:/mnt/data \
    -e TPOT_GENERATIONS=1 \
    -e TPOT_POPULATION_SIZE=1 \
    -e TPOT_TEST_SIZE=0.2 \
    ukgovdatascience/govuk-taxonomy-ml-image:0.1.1 python TPOT_allgovuk.py

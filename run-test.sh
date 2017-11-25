#!/bin/bash

docker run -i --rm \
    -v /data:/mnt/data \
    -e TPOT_GENERATIONS=1 \
    -e TPOT_POPULATION_SIZE=1 \
    -e TPOT_VERBOSITY=3 \
    ukgovdatascience/govuk-taxonomy-ml-image:latest python TPOT_allgovuk.py

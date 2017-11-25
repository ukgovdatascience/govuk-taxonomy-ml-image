#!/bin/bash

docker run -i --rm \
    -v /data:/mnt/data \
    -e TPOT_GENERATIONS=5 \
    -e TPOT_POPULATION_SIZE=20 \
    -e TPOT_TEST_SIZE=0.2 \
    -e TPOT_VERBOSITY=3 \
    -e TPOT_NUMJOBS=1 \
    ukgovdatascience/govuk-taxonomy-ml-image:latest python TPOT_allgovuk.py

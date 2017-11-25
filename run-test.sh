#!/bin/bash

docker run -i --rm \
    -v /data:/mnt/data \
    -e TPOT_GENERATIONS=1 \
    -e TPOT_POPULATION_SIZE=1 \
    -e TPOT_TEST_SIZE=0.2 \
    -e TPOT_VERBOSITY=3 \
    -e TPOT_NUMJOBS=1 \
    ukgovdatascience/govuk-taxonomy-ml-image:0.1.1 python TPOT_allgovuk.py

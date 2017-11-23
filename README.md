# GOV.UK Taxonomy machine learning image

## Contents

This repo contains the following:

* Source code for running automated machine learning using the python TPOT framework.
* A Dockerfile for building a Docker container to run a python3.4.6 environment.

## Instructions

### Getting started

Once volume mounts have been properly configured, it should be possible to launch the container and TPOT process simply by executing the `run.sh` script.

### Building the Docker container

This github repository has been linked to a docker hub repository allowing the container to be automatically built following each push on master to github. The latest container will be pulled automatically from docker hub when the `run.sh` script is run. More specifically when a `docker run` or `docker pull` command is issued.

During experimentation, you may also want to build the container locally (or remotely), this can be done with:

```
# Where <tag> is the version number or nominally 'latest'

docker build -t ukgovdatascience/govuk-taxonomy-ml-image:<tag> .
```

### Environment variables and docker mounts

No data are stored in the docker image itself, so these must be made available to the container by mounting a volume. This is done automatically in the `run.sh`, which connects the $DATADIR location with an internal mount point on the docker container (`/mnt/data`). $DATADIR should thus point at the location on the local machine where the data are stored.



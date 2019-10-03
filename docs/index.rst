.. OpenSteer documentation master file, created by
   sphinx-quickstart.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

OpenSteer Project Documentation
====================================================================

Table of Contents:

.. toctree::
   :maxdepth: 2


Indices & Tables
================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Digital Ocean
=============

https://docs.docker.com/machine/drivers/digital-ocean/

list images::

    doctl compute image list-distribution

list sizes::

    doctl compute size  list

list regions::

    doctl compute region list

Create Machine::

    docker-machine create \
        --driver digitalocean \
        --digitalocean-access-token TOKEN \
        --digitalocean-image IMAGE_NAME \
        --digitalocean-size SIZE \
        --digitalocean-region REGION \
        MACHINE_NAME


encodeproject
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy| |code_climate_maintainability| |pip| |downloads|

Python package wrapping some of the encode project APIs.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install encodeproject

Tests Coverage
----------------------------------------------
Since some software handling coverages sometimes
get slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|

Usage Examples
-----------------------------------------------
The package contains both methods to run queries on the `Encode Project APIs <https://www.encodeproject.org/help/rest-api/>`_ and
methods to filter the responses. Every available method has a comprehensive docstring attached to it, so I welcome you to
read the source code. 

Queries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The library currently offers to query methods that already integrate some filtering properties:
one for the `experiments <https://www.encodeproject.org/experiments/>`_
and one for the `biosamples <https://www.encodeproject.org/biosamples/>`_.

For querying the experiments you can run the following:

.. code:: python

    from encodeproject import experiment

    my_experiment_query_response = experiment(
        assembly="hg19", # The assembly label, for instance "hg19".
        status="released", # The release status, can be either "released", "archived" or "revoked".
        cell_line="HepG2", # The label for the chosen cell line for instance "HepG2".
        target="ARID3A", # The target name, for instance "ARID3A".
        parameters = {} # Additional query parameters
    )

All parameters are optional, they just act as additional filters.

For querying the biosamples you can run the following:

.. code:: python

    from encodeproject import biosample

    my_biosample_query_response = biosample(
        accession="ENCSR000EDP", # The accession code for the desired biosample
    )

For running multiple queries for biosamples at once you can run the following:

.. code:: python

    from encodeproject import biosamples

    responses = biosamples(
        accessions=["ENCSR000EDP", "ENCSR030EDP", "ENCSR067EDP"], # The accessions code for the desired biosamples
    )

Filters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Since the response files can get quite big and hard to read, I've prepared also a couple filter functions.

For filtering the accessions codes from an experiment response you can use:

.. code:: python

    from encodeproject import accessions

    codes = accessions(my_experiment_query_response)


For filtering the download URLs from a biosample response you can use:

.. code:: python

    from encodeproject import download_urls

    codes = download_urls(my_biosample_query_response)


Utilities
-----------------------------------------

Download utility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
I've added also a method to download from a given URL, showing a loading bar, based on `this answer from StackOverflow <https://stackoverflow.com/questions/37573483/progress-bar-while-download-file-over-http-with-requests/37573701#37573701>`_.

.. code:: python

    from encodeproject import download

    download("https://encode-public.s3.amazonaws.com/2012/07/01/074e1b37-2be1-4f6a-aa42-6c512fd1834b/ENCFF000XOW.bigWig")


Sample to DataFrame instruction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Utility to convert a sample to a relatively simple `pandas DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_.

.. code:: python

    from encodeproject import biosample_to_dataframe

    df = biosample_to_dataframe(my_biosample_query_response)


Issues and Feature Requests
-----------------------------------------
This library started out of necessity to script some queries on the encodeproject. If you need some specific feature
that isn't currently already offered by the library, please do proceed with a pull request (quickest way: add the feature yourself
and push it on the library) or alternatively you can open an issue and when I'll get the time I'll see to it.

.. |travis| image:: https://travis-ci.org/LucaCappelletti94/encodeproject.png
   :target: https://travis-ci.org/LucaCappelletti94/encodeproject
   :alt: Travis CI build

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_encodeproject&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_encodeproject
    :alt: SonarCloud Quality

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_encodeproject&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_encodeproject
    :alt: SonarCloud Maintainability

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_encodeproject&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_encodeproject
    :alt: SonarCloud Coverage

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/encodeproject/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/encodeproject?branch=master
    :alt: Coveralls Coverage

.. |pip| image:: https://badge.fury.io/py/encodeproject.svg
    :target: https://badge.fury.io/py/encodeproject
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/encodeproject
    :target: https://pepy.tech/badge/encodeproject
    :alt: Pypi total project downloads 

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/0f5c4026d3ec4cadb0d4a51f83235a2c
    :target: https://www.codacy.com/manual/LucaCappelletti94/encodeproject?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LucaCappelletti94/encodeproject&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/8e5a18a61e3a05f79af0/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/encodeproject/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/8e5a18a61e3a05f79af0/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/encodeproject/test_coverage
    :alt: Code Climate Coverate

=============================
django-hvad-cleanerversion
=============================

.. image:: https://badge.fury.io/py/djang-hvad-cleanerversion.svg
    :target: https://badge.fury.io/py/djang-hvad-cleanerversion

.. image:: https://travis-ci.org/rasca/djang-hvad-cleanerversion.svg?branch=master
    :target: https://travis-ci.org/rasca/djang-hvad-cleanerversion

.. image:: https://codecov.io/gh/rasca/djang-hvad-cleanerversion/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/rasca/djang-hvad-cleanerversion

Integration of django-hvad and cleanerversion

Documentation
-------------

The full documentation is at https://djang-hvad-cleanerversion.readthedocs.io.

Quickstart
----------

Install django-hvad-cleanerversion::

    pip install djang-hvad-cleanerversion

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'hvad_cleanerversion.apps.HvadCleanerversionConfig',
        ...
    )

Add django-hvad-cleanerversion's URL patterns:

.. code-block:: python

    from hvad_cleanerversion import urls as hvad_cleanerversion_urls


    urlpatterns = [
        ...
        url(r'^', include(hvad_cleanerversion_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage

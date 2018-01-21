=====
Usage
=====

To use django-hvad-cleanerversion in a project, add it to your `INSTALLED_APPS`:

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

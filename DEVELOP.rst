Using the development buildout
==============================

Requires `uv <https://docs.astral.sh/uv/getting-started/installation/>`_.

Create a virtualenv in ``.venv``, install requirements and run buildout::

    $ make

Start Plone in foreground::

    $ make run

List all available targets::

    $ make help


Running tests
-------------

    $ tox

list all tox environments:

    $ tox -l
    py38-Plone52
    build_instance
    code-analysis
    lint-py38
    coverage-report

run a specific tox env:

    $ tox -e py38-Plone52

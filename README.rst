.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://github.com/IMIO/imio.smartweb.policy/workflows/Tests/badge.svg
    :target: https://github.com/IMIO/imio.smartweb.policy/actions?query=workflow%3ATests
    :alt: CI Status

.. image:: https://coveralls.io/repos/github/IMIO/imio.smartweb.policy/badge.svg?branch=main
    :target: https://coveralls.io/github/IMIO/imio.smartweb.policy?branch=main
    :alt: Coveralls

.. image:: https://img.shields.io/pypi/v/imio.smartweb.policy.svg
    :target: https://pypi.python.org/pypi/imio.smartweb.policy/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/imio.smartweb.policy.svg
    :target: https://pypi.python.org/pypi/imio.smartweb.policy
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/imio.smartweb.policy.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/imio.smartweb.policy.svg
    :target: https://pypi.python.org/pypi/imio.smartweb.policy/
    :alt: License


====================
imio.smartweb.policy
====================

Policies to setup imio.smartweb

Features
--------

- **Site policy**: GenericSetup profiles (default, multilingual, testing, demo, uninstall) that configure a complete SmartWeb Plone site for Belgian municipalities.
- **Content type configuration**: Pre-configured Plone content types (Collection, Document, Event, File, Folder, Image, Link, News Item).
- **Registry settings**: SmartWeb-specific registry entries for timezone (Europe/Brussels), auto-publishing, autoscaling, caching, and message viewlets.
- **Viewlet management**: Custom portal layout (header, footer, navigation) with SmartWeb-specific viewlets replacing default Plone ones.
- **Site setup handlers**: Post-installation setup — removes default Plone content, creates "I am" / "I find" navigation folders with dynamic links.
- **GDPR & accessibility**: Registers GDPR consent text, cookie policy, and AnySurfer accessibility statements (templated per organisation).
- **Multilingual support**: Optional multilingual profile integrating plone.app.multilingual.
- **Authentication**: Upgrade steps for Keycloak/OIDC group configuration and Kimug user migration.
- **Search**: Solr integration (collective.solr) with Tika indexing enabled.
- **Upgrade steps**: Incremental upgrade steps to migrate existing instances across package versions.



Installation
------------

Install imio.smartweb.policy by adding it to your buildout::

    [buildout]

    ...

    eggs =
        imio.smartweb.policy


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/imio/imio.smartweb.policy/issues
- Source Code: https://github.com/imio/imio.smartweb.policy


License
-------

The project is licensed under the GPLv2.

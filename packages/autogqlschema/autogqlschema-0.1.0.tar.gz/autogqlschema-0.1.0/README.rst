autogqlschema
==============

.. image:: https://readthedocs.org/projects/autogqlschema/badge/?version=latest
    :target: https://autogqlschema.readthedocs.org
    :alt: Documentation

.. image:: https://github.com/AWhetter/autogqlschema/actions/workflows/main.yml/badge.svg?branch=main
    :target: https://github.com/AWhetter/autogqlschema/actions/workflows/main.yml?query=branch%3Amain
    :alt: Github Build Status

.. image:: https://img.shields.io/pypi/v/autogqlschema.svg
    :target: https://pypi.org/project/autogqlschema/
    :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/autogqlschema.svg
    :target: https://pypi.org/project/autogqlschema/
    :alt: Supported Python Versions

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black
    :alt: Formatted with Black

A Sphinx extension for automatically documenting GraphQL schemas.


Getting Started
---------------

The following steps will walk through how to add ``autogqlschema`` to an existing Sphinx project.
For instructions on how to set up a Sphinx project,
see Sphinx's documentation on
`Getting Started <https://www.sphinx-doc.org/en/master/usage/quickstart.html>`_.


Installation
~~~~~~~~~~~~

``autogqlschema`` can be installed through pip:

.. code-block:: bash

    pip install autogqlschema

Next, add ``autogqlschema`` to the ``extensions`` list in your Sphinx project's `conf.py`.

.. code-block:: python

    extensions.append("autogqlschema")


Usage
-----

Schema documentation is generated from GraphQL schema files using the ``autogqlschema`` directive.

In the following example, documentation is generated from ths file structure.

.. code-block:: none

    myrepo
    ├── doc
        ├── conf.py
        └── index.rst
    └── src
        └── mypackage
            ├── schema
            │   ├── __init__.py
            │   ├── 01_schema.graphql
            │   └── 02_books.graphql
            └── __init__.py

This schema can be generated with the following reStructuredText:

.. code-block:: rst

      .. autogqlschema::
         :root-dir: ../src/mypackage/schema
         :source-files: *.graphql

Or:

.. code-block:: rst

      .. autogqlschema::
         :root-dir: ../src/mypackage/schema
         :source-files: 01_schema.graphql, 02_books.graphql

For more detailed usage, see the documentation:
https://autogqlschema.readthedocs.io/en/latest/


Contributing
------------

Running the tests
~~~~~~~~~~~~~~~~~

Tests are executed through `tox <https://tox.readthedocs.io/en/latest/>`_.

.. code-block:: bash

    tox


Code Style
~~~~~~~~~~

Code is formatted using `black <https://github.com/python/black>`_.

You can check your formatting using black's check mode:

.. code-block:: bash

    tox -e format

You can also get black to format your changes for you:

.. code-block:: bash

    tox -e format -- src/ tests/


Release Notes
~~~~~~~~~~~~~

Release notes are managed through `towncrier <https://towncrier.readthedocs.io/en/stable/index.html>`_.
When making a pull request you will need to create a news fragment to document your change:

.. code-block:: bash

    tox -e release_notes -- create --help


Versioning
----------

We use `SemVer <https://semver.org/>`_ for versioning.
For the versions available, see the `tags on this repository <https://github.com/AWhetter/autogqlschema/tags>`_.


License
-------

This project is licensed under the MIT License.
See the `LICENSE.rst <LICENSE.rst>`_ file for details.

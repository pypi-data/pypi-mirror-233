Overview
========

xmlcoll is a python package for working with collections of items.
The items have heterogeneous data stored as
`properties` in a dictionary with keys given by a
name and optional tags.  The package API has routines to write data to and
retrieve data from `XML <https://www.w3.org/XML/>`_ and to validate that
XML against a schema.

|pypi| |doc_stat| |license| |test| |lint| |lint-test| |black|

Installation
------------

Install from `PyPI <https://pypi.org/project/xmlcoll>`_ with pip by
typing in your favorite terminal::

    $ pip install xmlcoll

Usage
-----

To get familiar with xmlcoll, please see the tutorial Jupyter
`notebook <https://github.com/mbradle/xmlcoll_tutorial>`_.

Authors
-------

- Bradley S. Meyer <mbradle@g.clemson.edu>

Documentation
-------------

The project documentation is available at `<https://xmlcoll.readthedocs.io>`_.

Contribute
----------

- Issue Tracker: `<https://github.com/mbradle/xmlcoll/issues/>`_
- Source Code: `<https://github.com/mbradle/xmlcoll/>`_

License
-------

The project is licensed under the GNU Public License v3 (or later).

.. |pypi| image:: https://badge.fury.io/py/xmlcoll.svg 
    :target: https://badge.fury.io/py/xmlcoll
.. |license| image:: https://img.shields.io/github/license/mbradle/xmlcoll
    :alt: GitHub
.. |doc_stat| image:: https://readthedocs.org/projects/xmlcoll/badge/?version=latest
    :target: https://xmlcoll.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. |test| image:: https://github.com/mbradle/xmlcoll/actions/workflows/test.yml/badge.svg?branch=main&event=push
        :target: https://github.com/mbradle/xmlcoll/actions/workflows/test.yml
.. |lint| image:: https://img.shields.io/badge/linting-pylint-yellowgreen
    :target: https://github.com/pylint-dev/pylint
.. |lint-test| image:: https://github.com/mbradle/xmlcoll/actions/workflows/lint.yml/badge.svg?branch=main&event=push
        :target: https://github.com/mbradle/xmlcoll/actions/workflows/lint.yml 
.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black


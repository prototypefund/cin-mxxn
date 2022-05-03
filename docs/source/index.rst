.. mixxin documentation master file, created by
   sphinx-quickstart on Wed Jan  5 11:10:27 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The MXXN Framework!
===================

MXXN is an easy to use framework for rapid web application
development. To avoid reinventing the wheel, we use a selection
of well maintained professional software packages and we try to
keep dependencies as low as possible.

We uses `SQLAlchemy`_ as ORM and `Alembic`_ for database schema
versioning. For the realization of the REST API we use `Falcon`_,
the frontend rely on `Lit`_ and TypeScript.

.. _SQLAlchemy: https://www.sqlalchemy.org/
.. _Alembic: https://alembic.sqlalchemy.org
.. _Falcon: https://falcon.readthedocs.io
.. _Lit: https://lit.dev/

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    cli
    routes
    settings
    logging
    api/api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

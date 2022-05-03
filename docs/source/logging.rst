Logging
=======

The Mxxn framework provides its own function to create an
context based application logger. The logger name is in format
*mxxn.<package>.<context>*. In framework packages each log entry
should be assigned to a context. The respective context should be
one of the following:

+--------------+----------------------------------------+
| Context      | Description                            |
+==============+========================================+
| settings     | Settings specific logging              |
+--------------+----------------------------------------+
| filesystem   | Context for filesystem interactions    |
+--------------+----------------------------------------+
| database     | Database specific logging              |
+--------------+----------------------------------------+
| registration | Context of component registration like |
|              | resource or static files               |
+--------------+----------------------------------------+
| request      | Context for requests                   |
+--------------+----------------------------------------+
| template     | Constext for template rendering        |
+--------------+----------------------------------------+

If none of these contexts meets your needs, then you can choose your own.

Usage:

.. code-block:: python

  from mxxn.logging import logger

  log = logger('some_context')
  log.error('test error')

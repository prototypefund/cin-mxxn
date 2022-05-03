Command Line Interface
======================

When installing the MXXN framework, a CLI programm is registered as
console scripts under the name mxxr. This command line program can
be used to manage the database schema of the Mxxn, Mxn or MxnApp packages.
For this purpose, a reduced selection of Alembic command
line functions has been added as CLI argument 'mxxr db'.
For more information use the following command:

.. code-block::

   $ mxxr db -h
   usage: mxxr db [-h]
   {init,upgrade,downgrade,branches,current,heads,history,merge,show,revision}

    positional arguments:
      {init,upgrade,downgrade,branches,current,heads,history,merge,show,revision}

        init        Initialize the mxn or mxnapp branch.
        upgrade     Upgrade to a later version.
        downgrade   Revert to a previous version.
        branches    Show current branch points.
        current     Display the current revision for a database.
        heads       Show current available heads in the script directory.
        history     List changeset scripts in chronological order.
        merge       Merge two revisions together. Creates a new migration file.
        show        Show the revision(s) denoted by the given symbol.
        revision    Create a new revision file.

    options:
      -h, --help            show this help message and exit

.. note::

    To avoid errors, only a few command line options are available in
    productive use. Only if the extra_require option develop is installed,
    the features for managing and creating database schema revisions
    become visible.

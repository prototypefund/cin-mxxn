Settings
========

Like most Python packages, the Mxxn framework uses a settings file in INI
format. This has the advantage that there is the possibility of using only
one settings file for Mxxn, Alembic, Supervisor, Gunicorn etc.

Mxxn itself reads the *mxxn* section and the *sqlalchemy_url* variable of
the *alembic* section of the settings file.

.. note::
    If an extra settings file is used for alembic, then the alembic section
    with the sqlalchemy_url variable must still be present in the Mxxn
    settings file.

The Mxxn settings file can be passed to the framework via the environment
variable *MXXN_SETTINGS*. If the variable is not used, the settings.ini file
is searched for in the current working directory. If no settings file is
applied, the default settings of the Mxxn framework are used.

List of variables:

+-------------+------------------+-------+--------------------------+
| Section     | Variable         | Type  | Description              |
+=============+==================+=======+==========================+
| mxxn        | enabled_mxns     | list  | List of enabled mxns     |
+-------------+------------------+-------+--------------------------+
| mxxn        | app_path         | str   | Application directory    |
+-------------+------------------+-------+--------------------------+
| mxxn        | data_path        | str   | Data directory           |
+-------------+------------------+-------+--------------------------+
| alembic     | sqllchemy_url    | str   | SQLAlchemy database url  |
+-------------+------------------+-------+--------------------------+

enabled_mxns
  It is possible to activate only specific Mxns in the settings file.
  If the *enabled_mxns* variable of the settings file is not set,
  all installed Mxns will be activated. To deactivate all installed mxns,
  an empty list can be set in the settings file.

app_path         
  The application path is the location where the runtime data of the
  application are stored. This is usually where the settings.ini and
  the data folder are located, which contains, for example, the SQLite
  database, if used. If the app_path variable of the settings file is
  not set, the current working directory at the time of the application
  start will be used.

data_path
  The Data folder is normally located in the application path and
  contains, for example, the SQLite database, if one is used. The files
  folder, in which the uploaded files are stored, is also located there.
  If the data_path variable of the settings file is not set, the
  *app_path/data* will be used.

sqllchemy_url
  The database URL is taken from the *sqlalchemy_url* variable of the
  *alembic* section of the settings file. If this was not set, the
  default URL *sqlite:///<data_path>/mxxn.db* will be used.

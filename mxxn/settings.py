
"""
The Settings module is used to access the application settings.

Like most Python packages, the Mixxin framework uses a settings file in INI
format. This has the advantage that there is the possibility of using only
one settings file for Mixxin, Alembic, Supervisor, Uvicorn etc.

Mixxin itself reads the `mixxin` section and the `sqlalchemy_url` variable of
the `alembic` section of the settings file.

!!! note
    If an extra settings file is used for alembic, then the alembic section
    with the sqlalchemy_url variable must still be present in the Mixxin
    settings file.

The Mixxin settings file can be passed to the framework via the environment
variable `MIXXIN_SETTINGS`. If the variable is not used, the settings.ini file
is searched for in the current working environment. If no settings file is
applied, the default settings of the Mixxin framework are used.
"""

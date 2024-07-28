import logging

from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig

from sqlalchemy import Engine
from sqlalchemy.schema import CreateSchema
from sqlalchemy_utils import create_database, database_exists

from app import config

from app.database.core import Base


log = logging.getLogger(__file__)


def version_schema(script_location: str):
    """Applies alembic versioning to schema."""

    # add it to alembic table
    alembic_cfg = AlembicConfig(config.ALEMBIC_INI_PATH)
    alembic_cfg.set_main_option("script_location", script_location)
    alembic_command.stamp(alembic_cfg, "head")


def get_core_tables():
    """Fetches tables that belong to the 'app_core' schema."""
    core_tables = []
    for _, table in Base.metadata.tables.items():
        if table.schema == "app_core":
            core_tables.append(table)
    return core_tables


def init_database(engine: Engine):
    """Initializes the database."""
    if not database_exists(str(config.SQLALCHEMY_DATABASE_URI)):
        create_database(str(config.SQLALCHEMY_DATABASE_URI))

    schema_name = "app_core"
    # if not engine.dialect.has_schema(engine, schema_name):
    with engine.connect() as connection:
        connection.execute(CreateSchema(schema_name))

    tables = get_core_tables()

    Base.metadata.create_all(engine, tables=tables)

    version_schema(script_location=config.ALEMBIC_REVISION_PATH)


if __name__ == "__main__":
    from app.database.core import engine

    init_database(engine)

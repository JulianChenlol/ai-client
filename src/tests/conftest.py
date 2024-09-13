import pytest
from sqlalchemy_utils import drop_database, database_exists
from starlette.config import environ
from starlette.testclient import TestClient

environ["DATABASE_NAME"] = "test"

from app import config
from app.database.core import engine
from app.database.manage import init_database

from .database import Session


@pytest.fixture(scope="session")
def db():
    if database_exists(str(config.SQLALCHEMY_DATABASE_URI)):
        drop_database(str(config.SQLALCHEMY_DATABASE_URI))

    init_database(engine)
    schema_engine = engine.execution_options(
        schema_translate_map={
            None: "dispatch_organization_default",
            "dispatch_core": "dispatch_core",
        }
    )
    Session.configure(bind=schema_engine)
    yield
    drop_database(str(config.SQLALCHEMY_DATABASE_URI))


@pytest.fixture(scope="function", autouse=True)
def session(db):
    """
    Creates a new database session with (with working transaction)
    for test duration.
    """
    session = Session()
    session.begin_nested()
    yield session
    session.rollback()


@pytest.fixture(scope="function")
def client(testapp, session, client):
    yield TestClient(testapp)

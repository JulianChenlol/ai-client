from starlette.config import Config
from starlette.datastructures import Secret
from urllib import parse

config = Config(".env")
# database
DATABASE_HOSTNAME = config("DATABASE_HOSTNAME")
DATABASE_CREDENTIALS = config("DATABASE_CREDENTIALS", cast=Secret)
# this will support special chars for credentials
_DATABASE_CREDENTIAL_USER, _DATABASE_CREDENTIAL_PASSWORD = str(DATABASE_CREDENTIALS).split(":")
_QUOTED_DATABASE_PASSWORD = parse.quote(str(_DATABASE_CREDENTIAL_PASSWORD))
DATABASE_NAME = config("DATABASE_NAME", default="app")
DATABASE_PORT = config("DATABASE_PORT", default="5432")
DATABASE_ENGINE_POOL_SIZE = config("DATABASE_ENGINE_POOL_SIZE", cast=int, default=20)
DATABASE_ENGINE_MAX_OVERFLOW = config("DATABASE_ENGINE_MAX_OVERFLOW", cast=int, default=0)
# Deal with DB disconnects
# https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-disconnects
DATABASE_ENGINE_POOL_PING = config("DATABASE_ENGINE_POOL_PING", default=False)
SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{_DATABASE_CREDENTIAL_USER}:{_QUOTED_DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"

APP_JWT_SECRET = config("App_JWT_SECRET", default=None)
APP_JWT_ALG = config("App_JWT_ALG", default="HS256")
APP_JWT_EXP = config("App_JWT_EXP", cast=int, default=86400)  # Seconds

ALEMBIC_INI_PATH = config(
    "ALEMBIC_INI_PATH",
    default="src\\alembic\\alembic.ini",
)
ALEMBIC_REVISION_PATH = config(
    "ALEMBIC_REVISION_PATH",
    default="src\\alembic\\versions",
)
if __name__ == "__main__":
    print(SQLALCHEMY_DATABASE_URI)

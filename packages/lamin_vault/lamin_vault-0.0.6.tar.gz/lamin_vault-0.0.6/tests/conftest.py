import secrets
import string

import pytest
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine

from lamin_vault.utils._lamin_dsn import LaminDsn


def base62(n_char: int) -> str:
    """Like nanoid without hyphen and underscore."""
    alphabet = string.digits + string.ascii_letters.swapcase()
    id = "".join(secrets.choice(alphabet) for i in range(n_char))
    return id


@pytest.fixture(scope="session")
def run_id():
    return base62(6)


@pytest.fixture(scope="session")
def db_name(run_id):
    return f"instance-ci-{run_id}"


@pytest.fixture(scope="session")
def db_url(db_name):
    connection = None
    user = "postgres"
    password = "JC^0ozMGprQdHrSv"
    host = "34.123.208.102"
    port = "5432"

    try:
        # Connect to the default database to create a new temporary one
        connection_url = LaminDsn.build(
            scheme="postgresql",
            user=user,
            password=password,
            host=host,
            database="postgres",
        )

        engine = create_engine(connection_url)
        connection = engine.raw_connection()
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        # Create a new temporary database
        cursor.execute(f'DROP DATABASE IF EXISTS "{db_name}";')
        cursor.execute(f'CREATE DATABASE "{db_name}";')

        # Yield the URL of the temporary database
        yield LaminDsn.build(
            scheme="postgresql",
            user=user,
            password=password,
            host=host,
            port=port,
            database=db_name,
        )

    finally:
        if connection:
            # Terminate open sessions
            cursor.execute(
                sql.SQL(
                    "SELECT pg_terminate_backend(pg_stat_activity.pid) "
                    "FROM pg_stat_activity "
                    f"WHERE datname = '{db_name}' "
                    "AND pid <> pg_backend_pid();"
                )
            )

            # Drop the temporary database after the test function has completed
            cursor.execute(f'DROP DATABASE IF EXISTS "{db_name}";')
            connection.close()


@pytest.fixture(scope="session")
def instance_context(db_url, db_name):
    from lamindb_setup._delete import delete
    from lamindb_setup._init_instance import init
    from lamindb_setup._settings import settings

    instance_name = db_name
    try:
        init(name=instance_name, storage="s3://lamindata", db=db_url)  # _vault=False

        yield {
            "instance_name": instance_name,
            "instance_id": str(settings.instance.id),
            "account_id": str(settings.user.uuid),
            "access_token": settings.user.access_token,
            "db_url": db_url,
        }
    finally:
        delete(instance_name=instance_name, force=True)

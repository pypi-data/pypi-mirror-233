import psycopg2

from lamin_vault.client._create_vault_client import (
    create_vault_admin_client,
    create_vault_authenticated_client,
)
from lamin_vault.client._init_instance_vault import init_instance_vault
from lamin_vault.client.postgres._get_db_from_vault import get_db_from_vault
from lamin_vault.utils._lamin_dsn import LaminDsnModel


def test_get_db_from_vault(instance_context):
    instance_id = instance_context["instance_id"]
    admin_account_id = instance_context["account_id"]
    access_token = instance_context["access_token"]
    db_url = instance_context["db_url"]

    vault_client_test = create_vault_authenticated_client(
        access_token=access_token, server_side=True
    )
    vault_admin_client_test = create_vault_admin_client(
        access_token=access_token, instance_id=instance_id, server_side=True
    )

    db_dsn_admin = LaminDsnModel(db=db_url)

    role_name = f"{instance_id}-{admin_account_id}-db"

    init_instance_vault(
        vault_admin_client=vault_admin_client_test,
        instance_id=instance_id,
        admin_account_id=admin_account_id,
        db_host=db_dsn_admin.db.host,
        db_port=db_dsn_admin.db.port,
        db_name=db_dsn_admin.db.database,
        vault_db_username=db_dsn_admin.db.user,
        vault_db_password=db_dsn_admin.db.password,
    )

    db_dsn = get_db_from_vault(
        vault_client=vault_client_test,
        scheme="postgresql",
        host=db_dsn_admin.db.host,
        port=db_dsn_admin.db.port,
        name=db_dsn_admin.db.database,
        role=role_name,
    )

    try:
        connection = psycopg2.connect(dsn=db_dsn)
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        assert (
            result[0] == 1
        ), "Should be able to execute a query with the obtained credentials."
    finally:
        # Close the connection and cursor
        cursor.close()
        connection.close()
        # Delete the created resources
        role_name = f"{instance_id}-{admin_account_id}-db"
        policy_name = f"{role_name}-policy"
        connection_config_path = f"database/config/{instance_id}"

        vault_admin_client_test.secrets.database.delete_role(name=role_name)
        vault_admin_client_test.sys.delete_policy(name=policy_name)
        vault_admin_client_test.delete(connection_config_path)

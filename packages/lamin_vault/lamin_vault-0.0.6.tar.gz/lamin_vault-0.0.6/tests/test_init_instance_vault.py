from lamin_vault.client._create_vault_client import (
    create_vault_admin_client,
    create_vault_authenticated_client,
)
from lamin_vault.client._init_instance_vault import init_instance_vault
from lamin_vault.client.postgres._connection_config_db_exists import (
    connection_config_db_exists,
)
from lamin_vault.client.postgres._role_and_policy_exist import role_and_policy_exist
from lamin_vault.utils._lamin_dsn import LaminDsnModel


def test_init_instance_vault(instance_context):
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

    db_dsn = LaminDsnModel(db=db_url)

    try:
        init_instance_vault(
            vault_admin_client=vault_admin_client_test,
            instance_id=instance_id,
            admin_account_id=admin_account_id,
            db_host=db_dsn.db.host,
            db_port=db_dsn.db.port,
            db_name=db_dsn.db.database,
            vault_db_username=db_dsn.db.user,
            vault_db_password=db_dsn.db.password,
        )

        # Verify connection configuration exists
        assert connection_config_db_exists(
            vault_client=vault_client_test, instance_id=instance_id
        ), "Connection configuration should exist in vault."

        # Verify connection admin role and policy exist
        assert role_and_policy_exist(
            vault_client=vault_client_test,
            instance_id=instance_id,
            account_id=admin_account_id,
        ), "Admin role and policy should exist in vault."

        # Verify role and policy exist
        role_name = f"{instance_id}-{admin_account_id}-db"
        policy_name = f"{role_name}-policy"

        assert (
            vault_client_test.secrets.database.read_role(name=role_name) is not None
        ), "Role should exist in vault."
        assert (
            vault_client_test.sys.read_policy(name=policy_name) is not None
        ), "Policy should exist in vault."

    finally:
        # Delete the created resources
        role_name = f"{instance_id}-{admin_account_id}-db"
        policy_name = f"{role_name}-policy"
        connection_config_path = f"database/config/{instance_id}"

        vault_admin_client_test.secrets.database.delete_role(name=role_name)
        vault_admin_client_test.sys.delete_policy(name=policy_name)
        vault_admin_client_test.delete(connection_config_path)

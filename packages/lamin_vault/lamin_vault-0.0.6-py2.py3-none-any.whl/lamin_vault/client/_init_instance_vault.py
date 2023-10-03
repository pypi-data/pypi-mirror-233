from lamin_vault.client.postgres._create_or_update_connection_config_db import (
    create_or_update_connection_config_db,
)
from lamin_vault.client.postgres._create_or_update_role_and_policy_db import (
    create_or_update_role_and_policy_db,
)


def init_instance_vault(
    vault_admin_client,
    instance_id,
    admin_account_id,
    db_host,
    db_port,
    db_name,
    vault_db_username,
    vault_db_password,
):
    create_or_update_connection_config_db(
        vault_admin_client=vault_admin_client,
        instance_id=instance_id,
        db_host=db_host,
        db_port=db_port,
        db_name=db_name,
        vault_db_username=vault_db_username,
        vault_db_password=vault_db_password,
    )

    admin_role_creation_statements = [
        "CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL"
        " '{{expiration}}';",
        "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO"
        ' "{{name}}";',
    ]

    create_or_update_role_and_policy_db(
        vault_admin_client=vault_admin_client,
        instance_id=instance_id,
        account_id=admin_account_id,
        creation_statements=admin_role_creation_statements,
    )

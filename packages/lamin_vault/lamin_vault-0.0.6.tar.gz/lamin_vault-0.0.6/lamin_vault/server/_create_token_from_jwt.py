from lamin_vault.utils._supabase_client import SbClientFromAccesToken


def create_token_from_jwt(vault_client_approle, access_token):
    # Verify JWT token and fetch policies
    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        supabase_client.auth.get_user(access_token)
        # TODO: Add some logic to fetch user instances
        # and create policies names that way: {instance_id}-{account_id}-db-policy
        policies = ["hcp-root"]

    # Create token to access vault
    created_token_response = vault_client_approle.auth.token.create(
        policies=policies, ttl="1h", wrap_ttl="1m"
    )
    vault_token = created_token_response["wrap_info"]["token"]

    return vault_token

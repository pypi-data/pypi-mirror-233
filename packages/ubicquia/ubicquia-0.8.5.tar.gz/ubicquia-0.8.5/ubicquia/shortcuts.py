"""Shortuct for common tools."""

import os
from .base import UbicquiaSession, TokenCache
from .client import Ubicquia


def ubicquia_instance(
    client_id: str = None,
    secret_key: str = None,
    username: str = None,
    password: str = None,
    token_cache: TokenCache = None,
) -> Ubicquia:
    """Create an instance of Ubicquia.

    If no parameters are provided, use Environment variables or raise error.

    Prefix env with `UBICQUIA_` all names in upper case. Use Ubicquia default
    names. Example:

    - UBICQUIA_CLIENT_ID
    - UBICQUIA_SECRET_KEY
    - UBICQUIA_USERNAME
    - UBICQUIA_PASSWORD

    Args:
        client_id: client id from platform.
        secret_key: secret from platform.
        username: username used in platform.
        password: password used in platform.
        token_cache: Implementaion of TokenCache. Can be None to shutdown the
            caching of token.

    Raises:
        ValueError: if no parameters are provided.
    """
    CLIENT_ID = client_id or os.getenv("UBICQUIA_CLIENT_ID")
    SECRET_KEY = secret_key or os.getenv("UBICQUIA_SECRET_KEY")
    USERNAME = username or os.getenv(
        "UBICQUIA_USERNAME",
    )
    PASSWORD = password or os.getenv("UBICQUIA_PASSWORD")
    if not CLIENT_ID:
        raise ValueError("No UBICQUIA_CLIENT_ID provided")
    if not SECRET_KEY:
        raise ValueError("No UBICQUIA_SECRET_KEY provided")
    if not USERNAME:
        raise ValueError("No UBICQUIA_USERNAME provided")
    if not PASSWORD:
        raise ValueError("No UBICQUIA_PASSWORD provided")
    session = UbicquiaSession(
        client_id=CLIENT_ID,
        client_secret=SECRET_KEY,
        username=USERNAME,
        password=PASSWORD,
        token_cache=token_cache,
    )
    return Ubicquia(session)


def list_nodes(ubicquia: Ubicquia) -> dict:
    """List all nodes in Ubicquia.

    Args:
        ubicquia: Ubicquia object.

    Returns:
        A List of nodes in this Ubicquia.
    """
    node_list = ubicquia.nodes.get_nodes_list()
    return node_list.model_dump(by_alias=True)

from api_compose.servers.prefixes import __API_SERVER_ONE_PREFIX__, __API_SERVER_ONE_PORT__


def setup_api_server_one():
    """Entrypoint for Jupyter server proxy"""
    return {
        'command': ['python', '-m', 'api_compose.servers.api_server_one.app', '{port}', '{base_url}' + __API_SERVER_ONE_PREFIX__],
        'port': __API_SERVER_ONE_PORT__,
        'absolute_url': True,
        'launcher_entry': {
            'enabled': True,
            'title': 'ApiServerOne',
        },
    }

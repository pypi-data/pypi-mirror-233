import sys

import connexion
from connexion.resolver import MethodViewResolver


def build_api_server_two(port, base_url):
    app = connexion.App(
        __name__,
        port=port,
        options={
            'swagger_ui': True,
            # Show Swagger UI at root
            'swagger_url': '/',
        }
    )
    app.add_api(
        'swagger.yaml',
        resolver=MethodViewResolver(
            'api_compose.servers.api_server_two.views',
        ),
        base_path=base_url
    )
    return app


if __name__ == '__main__':
    # run our standalone gevent server
    if len(sys.argv) == 3:
        port = sys.argv[1]
        port = int(port) if port else 8080

        base_url = f"{sys.argv[2]}"
        base_url = base_url if base_url else None
        app = build_api_server_two(port, base_url)
        app.run()
    else:
        raise ValueError('Usage: python ./app.py {port} {base_url}')

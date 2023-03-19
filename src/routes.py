from collections import namedtuple

import aiohttp_cors

from src import handlers

Route = namedtuple("Route", ["method", "path", "handler", "name"])

ROUTES = [
    Route(
        method="GET",
        path="/",
        handler=handlers.index,
        name="index"
    ),
]


def setup(app):

    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        }
    )

    for route in ROUTES:

        method, url, handler, name = route
        cors.add(app.router.add_route(method, url, handler, name=name))

        print(url.rsplit('{', 1)[0])

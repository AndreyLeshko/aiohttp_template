from aiohttp import web

from src import utils, settings

logger = settings.logger


async def index(request: web.Request) -> web.Response:

    # Для выполнения запроса из БД
    # result = request.app['db'].execute('...').fetchall()

    return web.Response(text=f"Welcome to the API")

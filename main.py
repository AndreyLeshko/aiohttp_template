import asyncio
import sys
import traceback

from aiohttp import web
import psycopg2

from src import settings, routes

logger = settings.logger


async def connect_db(app: web.Application):
    conn = psycopg2.connect(
        host=app["config"]["api"]["host"],
        port=app["config"]["api"]["port"],
        database=app["config"]["api"]["db_name"],
        user=app["config"]["api"]["username"],
        password=app["config"]["api"]["password"]
    )
    app["db"] = conn


async def disconnect_db(app: web.Application):
    if 'db' in app:
        app['db'].close()


def create_app() -> web.Application:
    app = web.Application()
    app['config'] = settings.read_config(settings.DEFAULT_CONFIG_PATH)

    routes.setup(app)

    app.on_startup.extend([connect_db])

    return app


async def shutdown(app: web.Application):
    await asyncio.gather(
        disconnect_db(app),
    )


def main():
    try:
        app = create_app()
        web.run_app(
            app,
            host='0.0.0.0',
            port=app["config"]["api"]["port"],
            access_log=logger
        )
    except Exception as ex:
        logger.critical(ex)
        logger.critical(traceback.format_exc())
    finally:
        try:
            shutdown(app)
        except NameError:
            sys.exit(1)


if __name__ == "__main__":
    main()

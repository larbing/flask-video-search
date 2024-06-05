import tornado
import tornado.wsgi
import asyncio
from app import create_app

async def main():
    app = create_app()
    container = tornado.wsgi.WSGIContainer(app)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(80)
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
import tornado
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
    #fastwsgi.run(wsgi_app=app,host='0.0.0.0',port=80,workers=4)
import fastwsgi
from app import create_app

if __name__ == '__main__':
    app = create_app()
    fastwsgi.run(wsgi_app=app,host='0.0.0.0',port=80,workers=4)
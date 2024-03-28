from flask import Flask,render_template,request

from .services import IndexService

app = Flask(__name__)
            
__solt__ = [app]

@app.route('/')
def index():
    serice = IndexService()
    return render_template('index.html')

@app.route('/search')
def search():
    keyword = request.args.get('q', '')
    service = IndexService()
    results = service.search(keyword)
    return render_template('search.html',keyword=keyword,results=results)
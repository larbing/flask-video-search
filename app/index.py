import math
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
    page_num = request.args.get('p', 1)
    service = IndexService()
    pageMaster = service.search(keyword,page_num=max(int(page_num),1))
    
    return render_template('search.html',keyword=keyword,pageMaster=pageMaster)
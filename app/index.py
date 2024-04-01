import math
from flask import Flask,Blueprint,render_template,request,url_for

from .services import IndexService


bp = Blueprint("index",__name__)

@bp.route('/')
def index():
    serice = IndexService()
    return render_template('index.html')

@bp.route('/search')
def search():
    keyword = request.args.get('q', '')
    page_num = request.args.get('p', 1)
    service = IndexService()
    pagination = service.search(keyword,page_num=max(int(page_num),1))
    return render_template('search.html',keyword=keyword,pageMaster=pagination,url_for=url_for)

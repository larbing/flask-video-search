import math
from flask import Flask,Blueprint,render_template,request,url_for

from .services import *
from .utils import getInt
from .requests import SearchRequest


bp = Blueprint("index",__name__)

indexService = IndexService()
dbService = DBService()

@bp.route('/')
def index():
    serice = IndexService()
    return render_template('index.html')

@bp.route('/search')
def search():
    keyword = request.args.get('q', '')
    page_num = getInt(request.args,'p',1)
    req = SearchRequest(name=keyword)
    pagination = indexService.search_by_request(req)
    return render_template('search.html',keyword=keyword,
                           pageMaster=pagination,
                           url_for=url_for,
                           get_info_by_id=dbService.get_info_by_id)
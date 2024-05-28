import math
from flask import Flask,Blueprint,render_template,Response,request,url_for

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

@bp.route('/player_links')
def links():

    name = request.args.get('name')
    if not name:
        return ""
    
    req = SearchRequest(name=name,page_size=1)
    pagination = indexService.search_by_request(req)
    if pagination.total < 1:
        return ""
    
    item = pagination.resutls[0]
    video_info = dbService.get_info_by_id(item.get('id'))
    
    html = render_template('links.html',video_info=video_info)
    
    # 创建一个Response对象
    response = Response(html, content_type='text/html; charset=utf-8')
    
    # 设置响应头
    response.headers['Access-Control-Allow-Origin'] = 'https://movie.douban.com'
    response.headers['Access-Control-Allow-Methods'] = ' GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = ' Content-Type'
    
    return response

@bp.route('/search')
def search():
    keyword = request.args.get('q', '')
    pageNo = getInt(request.args,'p',1)
    req = SearchRequest(name=keyword,page_no=pageNo)
    pagination = indexService.search_by_request(req)
    return render_template('search.html',keyword=keyword,
                           pageMaster=pagination,
                           url_for=url_for,
                           get_info_by_id=dbService.get_info_by_id)
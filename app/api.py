import json
import math
from flask import Blueprint,jsonify,Response,request

from .services import * 
from .utils import error_response,success_response,getInt
from .requests import SearchRequest

bp = Blueprint('api',__name__, url_prefix='/api')

dBService = DBService()
indexService = IndexService()

@bp.route("/hot_video_list")
def api_hot_video_list():
    json = """
    {
    "code": 0,
    "msg": "",
    "data": [
        {
		    "id" : "111111",
            "name": "Example Video",
            "image_url": "https://example.com/image.jpg",
            "video_type": "Movie",
            "content_type": "Action",
            "region": "USA",
            "release_date": "2023",
            "rating": "8",
            "plot": "An action-packed adventure.",
            "cast": "John Doe, Jane Smith",
            "director": "Director Name",
            "status": "Updated"
        }
    ]
}
""" 
    return json

@bp.post("/search")
def api_search():
    req = SearchRequest(**request.form)
    pagination = indexService.searchByRequest(req)
    return success_response(pagination.resutls,pagination.pageInfo)

@bp.post("/video_info")
def api_video_info():
    id = request.form.get('id')
    if not id:
        return error_response("id is required")
    
    video_info = dBService.get_info_by_id(id)
    if not video_info:
        return error_response("id is not exist")
    
    del video_info['links'],video_info['m3u8_links']
    return success_response(video_info)

@bp.post("/video_play_urls")
def api_video_play_urls():
    id = request.form.get('id')
    page_no = getInt(request.form, 'page_no',1)
    page_size = getInt(request.form,'page_size',10)

    id = request.form.get('id')
    if not id:
        return error_response("id is required")
    
    video_info = dBService.get_info_by_id(id)
    if not video_info:
        return error_response("id is not exist")
    
    links = video_info['links']
    start = (page_no - 1) * page_size
    end = min(start + page_size,len(links))
    page_total = math.ceil(len(links) / page_size)

    return success_response(links[start:end],
                            {"page_info":{"page_no":page_no,
                                          "page_size":page_size,
                                          "page_total":page_total}})
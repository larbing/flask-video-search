import json
import math
from flask import Blueprint,jsonify,Response,request

from .services import * 
from .utils import error_response,success_response,getInt,getString
from .requests import SearchRequest

bp = Blueprint('apiv2',__name__, url_prefix='/apiv2')

indexService           = IndexService()
bBService              = DBService()
channelSettingsService = ChannelSettingsService()

@bp.get("/getHome")
def api_get_home():
    return success_response({'ret': 1})

@bp.get("/getType")
def api_get_type():
    pid = getString(request.args,'pid','1')
    res = channelSettingsService.find_lists_by_pid(pid)
    return success_response(json.dumps(res),{'ret': 1})

@bp.get("/getVodWithPage")
def api_get_vod_with_page():
    req = SearchRequest()
    t_id = getInt(request.args,'d_type',10)
    req.content_type = channelSettingsService.find_name_by_id(t_id)
    req.page_size = getInt(request.args,'pageSize')
    req.page_no   = getInt(request.args,'page') + 1

    page = indexService.search_by_request(req)
    res = list()
    for p in page.resutls:
        item = dict()
        item['d_id'] = int(p.get('vid'))
        item['d_name'] = p.get('name')
        item['d_pic'] = p.get('image_url')
        item['d_type'] = str(t_id)
        item['d_remarks'] = p.get('status')
        item['d_score']= p.get('rating')
        res.append(item)

    return success_response(json.dumps(res),{'ret': 1,'total': page.total})

@bp.get("/getVodByPid")
def api_get_vod_by_pid():
    pass

@bp.get("/getVodById")
def api_get_vod_by_vid():
    vid = getString(request.args,'d_id')
    info = bBService.get_info_by_vid(vid)
    if info is None:
        return error_response('视频不存在',{'ret':0,'msg':'视频不存在'})
    
    res = dict()
    res['d_id'] = int(info.get('vid'))
    res['d_name'] = info.get('name')
    res['d_pic'] = info.get('image_url')
    res['d_remarks'] = info.get('status')
    res['d_score']= info.get('rating')
    res['d_starring'] = info.get('cast')
    res['d_lang'] = info.get('language')
    res['d_content'] = info.get('plot')
    res['d_type'] =  channelSettingsService.find_id_by_name(info.get('category'))
    res['d_area'] = info.get('region')
    res['d_year'] = info.get('release_date')
    res['d_playurl'] = "#".join(info.get('m3u8_links'))
    return success_response(json.dumps(res),{'ret': 1})
    

@bp.get("/search")
def api_search():
    return request.args.get('q')

@bp.post("/searchForHanZi")
def api_search_for_hanzi():
    keys= request.form.get('keys')
    page = indexService.search(keys)
    res = list()
    for p in page.resutls:
        item = dict()
        item['d_id'] = int(p.get('vid'))
        item['d_name'] = p.get('name')
        item['d_pic'] = p.get('image_url')
        item['d_remarks'] = p.get('status')
        item['d_score']= p.get('rating')
        res.append(item)

    return success_response(json.dumps(res),{'ret': 1,'total': page.total})
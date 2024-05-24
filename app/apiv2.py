import json
import math

from functools import wraps
from flask import Blueprint,jsonify,Response,request

from .services import * 
from .utils import error_response,success_response,getInt,getString
from .requests import SearchRequest

bp = Blueprint('apiv2',__name__, url_prefix='/apiv2')

indexService           = IndexService()
dbService              = DBService()
channelSettingsService = ChannelSettingsService()


def page_response(func):
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        page = func(*args, **kwargs)
        if not isinstance(page,Pagination):
            return page
        
        res = list()
        for p in page.resutls:
            item = dict()
            item['d_id'] = int(p.get('vid'))
            item['d_name'] = p.get('name')
            item['d_pic'] = p.get('image_url')
            item['d_remarks'] = p.get('status')
            item['d_score']= p.get('rating')
            item['updated'] = p.get('updated')
            res.append(item)

        return success_response(json.dumps(res),{'ret': 1,'total': page.total})
    return wrapper

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
    req.page_size = 150
    req.page_no   = getInt(request.args,'page') + 1

    page = indexService.search_by_request(req)
    resutls = sorted(page.resutls,key=lambda x:x.get('updated'),reverse=True)
    res = list()
    for p in resutls:
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
@page_response
def api_get_vod_by_pid():
    pid         = getInt(request.args,'pid',1)
    page_size   = getInt(request.args,'pageSize',20)
    page_start  = getInt(request.args,'page',0) * page_size
    types = ('movie','movie','tv','movie','movie')
    type =  types[pid]
    titles = DoubanService.get_hot_video_titles(type,page_limit=20,page_start=page_start)
    return indexService.search_by_titles(titles)

@bp.get("/getVodById")
def api_get_vod_by_vid():
    vid = getString(request.args,'d_id')
    info = dbService.get_info_by_vid(vid)
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
@page_response
def api_search_for_hanzi():
    keys= request.form.get('keys')
    return indexService.search(keys)

@bp.get("/getTodayUp")
@page_response
def get_today_update():
    req = SearchRequest()
    req.content_type = channelSettingsService.find_name_by_id(100)
    req.page_size = 50
    req.page_no   = getInt(request.args,'page') + 1

    page =  indexService.search_by_request(req,sort_by="updated")
    page.resutls = sorted(page.resutls,key=lambda x:x.get('release_date'),reverse=True)
    return page

@bp.get("/getHome")
def api_get_home():
    

    return """
        {
  "ret": 1,
  "msg": "成功！",
  "data": {
    "hotVods": [
 {
    "d_id": 1715481780,
    "d_name": "\u6b4c\u624b2024",
    "d_pic": "https://img.lzzyimg.com/upload/vod/20240511-1/1b5d6e202158b3f8ac8dc77571152eeb.jpg",
    "d_type": "1",
    "d_remarks": "\u66f4\u65b0\u81f3\u7b2c1\u671f",
    "d_score": "0.0"
  },
  {
    "d_id": 1715580805,
    "d_name": "\u9b54\u65b9\u65b0\u4e16\u754c",
    "d_pic": "https://img.lzzyimg.com/upload/vod/20240514-1/ae23912ce9337432a63d19ad80011678.jpg",
    "d_type": "1",
    "d_remarks": "\u66f4\u65b0\u81f3\u7b2c1\u671f",
    "d_score": "0.0"
  },
  {
    "d_id": 1715481779,
    "d_name": "\u707f\u70c2\u7684\u82b1\u56ed",
    "d_pic": "https://img.lzzyimg.com/upload/vod/20240427-1/18b48a60778d0d8f1271c116a41e321e.jpg",
    "d_type": "1",
    "d_remarks": "\u66f4\u65b0\u81f3\u7b2c3\u671f",
    "d_score": "0.0"
  },
  {
    "d_id": 1715472060,
    "d_name": "\u54c8\u5c14\u6ee8\u4e00\u4e5d\u56db\u56db",
    "d_pic": "https://img.lzzyimg.com/upload/vod/20240421-1/6b68f99b4be2fcc14997ee3808836b13.jpg",
    "d_type": "1",
    "d_remarks": "\u5df2\u5b8c\u7ed3",
    "d_score": "0.0"
  },
  {
    "d_id": 1715471991,
    "d_name": "\u6625\u8272\u5bc4\u60c5\u4eba",
    "d_pic": "https://img.lzzyimg.com/upload/vod/20240422-1/0694afdc8b468014aab3d0563a77a18f.jpg",
    "d_type": "1",
    "d_remarks": "\u5df2\u5b8c\u7ed3",
    "d_score": "0.0"
  },
  {
    "d_id": 1715471788,
    "d_name": "\u6211\u7684\u963f\u52d2\u6cf0",
    "d_pic": "https://img.lzzyimg.com/upload/vod/20240507-1/a1ab49729848576586220b45f9cf47e6.jpg",
    "d_type": "1",
    "d_remarks": "\u5df2\u5b8c\u7ed3",
    "d_score": "0.0"
  },
  {
    "d_id": 1715471791,
    "d_name": "\u5fae\u6697\u4e4b\u706b",
    "d_pic": "https://img.lzzyimg.com/upload/vod/20240427-1/c3cd23d2185f16e2165c7f0171d1fdc9.jpg",
    "d_type": "1",
    "d_remarks": "\u5df2\u5b8c\u7ed3",
    "d_score": "0.0"
  },
  {
    "d_id": 1715471708,
    "d_name": "\u4e0d\u53ef\u544a\u4eba",
    "d_pic": "https://img.lzzyimg.com/upload/vod/20240508-1/d0821d8b043217c5c2d5d5d973fb3774.jpg",
    "d_type": "1",
    "d_remarks": "\u5df2\u5b8c\u7ed3",
    "d_score": "0.0"
  },
  {
    "d_id": 1715472084,
    "d_name": "\u4e0d\u591f\u5584\u826f\u7684\u6211\u4eec",
    "d_pic": "https://img.lzzyimg.com/upload/vod/20240409-1/975b1d25db18f14c5aef3454508d81d7.jpg",
    "d_type": "1",
    "d_remarks": "\u5df2\u5b8c\u7ed3",
    "d_score": "8.5"
  }
    ],
    "stars": [
      {
        "t_id": 1,
        "t_name": "周润发",
        "t_key": "周润发",
        "t_des": "周润发",
        "t_enname": "周润发",
        "t_pic": "https://ming.webapicnd.com/upload/vodtopic/2023-02-25/202302251677318937.png",
        "t_content": "1955年（乙未年）5月18日（闰三月二十七） 香港南丫岛 中国周润发（Chow Yun Fat），1955年5月18日出生在香港南丫岛，籍贯广东开平，中国影视演员、摄影家，国家一级演员。1974年毕业于TVB艺员训练班，主演了《网中人》、《亲情》、《上海滩》等20余部剧集。1976年初涉影坛，在80年代凭《英雄本色》、《监狱风云》、《赌神》等电影成为香港“暴力美学”风格电影的代表人物之一&nbsp; 。90年代与成龙、周星驰并称为“双周一成”。1995年远赴好莱坞发展。主演了《安娜与国王》、《卧虎藏龙》",
        "t_hits": 3441
      },
      {
        "t_id": 747,
        "t_name": "何炅",
        "t_key": "hegui",
        "t_des": "hg",
        "t_enname": "hegui",
        "t_pic": "http://imgwx2.2345.com/dypcimg/star/img/f/0/76/photo_192x262.jpg?1509954497",
        "t_content": "",
        "t_hits": 0
      },
      {
        "t_id": 746,
        "t_name": "范冰冰",
        "t_key": "fanbingbing",
        "t_des": "fbb",
        "t_enname": "fanbingbing",
        "t_pic": "http://imgwx5.2345.com/dianyingimg/star/img/3/0/23/photo_192x262.jpg",
        "t_content": "",
        "t_hits": 0
      },
      {
        "t_id": 745,
        "t_name": "罗晋",
        "t_key": "luojin",
        "t_des": "lj",
        "t_enname": "luojin",
        "t_pic": "http://imgwx3.2345.com/dypcimg/star/img/d/0/1806/photo_192x262.jpg",
        "t_content": "",
        "t_hits": 0
      },
      {
        "t_id": 744,
        "t_name": "黄渤",
        "t_key": "huangbo",
        "t_des": "hb",
        "t_enname": "huangbo",
        "t_pic": "http://imgwx3.2345.com/dianyingimg/star/img/4/0/821/photo_192x262.jpg",
        "t_content": "",
        "t_hits": 0
      }
    ]
  }
}
    """
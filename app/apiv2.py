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

@bp.get("/getHome")
def api_get_home():
    return """
        {
  "ret": 1,
  "msg": "成功！",
  "data": {
    "hotVods": [
      {
        "d_id": 585,
        "d_name": "吞噬星空",
        "d_ldgletter": null,
        "d_enname": null,
        "d_pic": "http://pic.lzzypic.com/upload/vod/20220612-1/b6e9d8ca2b5dd5149e1ca2f9b6828927.jpg",
        "d_starring": null,
        "d_tag": null,
        "d_remarks": "更新至第118集",
        "d_area": null,
        "d_lang": null,
        "d_year": null,
        "d_type": "25",
        "d_level": null,
        "d_hits": 0,
        "d_score": "6.8",
        "d_time": null,
        "d_content": null,
        "d_playurl": null,
        "d_downurl": null,
        "isStore": 0
      },
      {
        "d_id": 991,
        "d_name": "斗破苍穹 年番",
        "d_ldgletter": null,
        "d_enname": null,
        "d_pic": "http://pic.lzzypic.com/upload/vod/20220731-1/49f05be1577eedcef89bf77415186537.jpg",
        "d_starring": null,
        "d_tag": null,
        "d_remarks": "更新至第95集",
        "d_area": null,
        "d_lang": null,
        "d_year": null,
        "d_type": "25",
        "d_level": null,
        "d_hits": 0,
        "d_score": "0.0",
        "d_time": null,
        "d_content": null,
        "d_playurl": null,
        "d_downurl": null,
        "isStore": 0
      },
      {
        "d_id": 980,
        "d_name": "凡人修仙传",
        "d_ldgletter": null,
        "d_enname": null,
        "d_pic": "http://pic.lzzypic.com/upload/vod/20220321-1/969d05badfc28453a78dcec09b221e0d.jpg",
        "d_starring": null,
        "d_tag": null,
        "d_remarks": "更新至第100集",
        "d_area": null,
        "d_lang": null,
        "d_year": null,
        "d_type": "25",
        "d_level": null,
        "d_hits": 0,
        "d_score": "7.9",
        "d_time": null,
        "d_content": null,
        "d_playurl": null,
        "d_downurl": null,
        "isStore": 0
      },
      {
        "d_id": 62407,
        "d_name": "斗罗大陆2：绝世唐门",
        "d_ldgletter": null,
        "d_enname": null,
        "d_pic": "http://pic.lzzypic.com/upload/vod/20230624-1/2734e7689124b78ca9ad7d35132ac6a8.jpg",
        "d_starring": null,
        "d_tag": null,
        "d_remarks": "更新至第47集",
        "d_area": null,
        "d_lang": null,
        "d_year": null,
        "d_type": "25",
        "d_level": null,
        "d_hits": 0,
        "d_score": "0.0",
        "d_time": null,
        "d_content": null,
        "d_playurl": null,
        "d_downurl": null,
        "isStore": 0
      },
      {
        "d_id": 315,
        "d_name": "完美世界",
        "d_ldgletter": null,
        "d_enname": null,
        "d_pic": "http://pic.lzzypic.com/upload/vod/20220319-1/704d65aebb2d59f07254b86e05c4384c.jpg",
        "d_starring": null,
        "d_tag": null,
        "d_remarks": "更新至第161集",
        "d_area": null,
        "d_lang": null,
        "d_year": null,
        "d_type": "25",
        "d_level": null,
        "d_hits": 0,
        "d_score": "6.9",
        "d_time": null,
        "d_content": null,
        "d_playurl": null,
        "d_downurl": null,
        "isStore": 0
      },
      {
        "d_id": 17653,
        "d_name": "孤注一掷",
        "d_ldgletter": null,
        "d_enname": null,
        "d_pic": "https://pic.lzzypic.com/upload/vod/20230806-1/1f18cae80ef1ddc6080fc0dea9a61ed4.jpg",
        "d_starring": null,
        "d_tag": null,
        "d_remarks": "HD",
        "d_area": null,
        "d_lang": null,
        "d_year": null,
        "d_type": "10",
        "d_level": null,
        "d_hits": 0,
        "d_score": "7.8",
        "d_time": null,
        "d_content": null,
        "d_playurl": null,
        "d_downurl": null,
        "isStore": 0
      },
      {
        "d_id": 76533,
        "d_name": "海王2：失落的王国",
        "d_ldgletter": null,
        "d_enname": null,
        "d_pic": "http://img.lzzyimg.com/upload/vod/20231225-1/ef0f6215c61cd60ccba40bdbb4d2741d.jpg",
        "d_starring": null,
        "d_tag": null,
        "d_remarks": "HD",
        "d_area": null,
        "d_lang": null,
        "d_year": null,
        "d_type": "5",
        "d_level": null,
        "d_hits": 0,
        "d_score": "6.7",
        "d_time": null,
        "d_content": null,
        "d_playurl": null,
        "d_downurl": null,
        "isStore": 0
      },
      {
        "d_id": 76423,
        "d_name": "三大队",
        "d_ldgletter": null,
        "d_enname": null,
        "d_pic": "http://img.lzzyimg.com/upload/vod/20231224-1/f3fad6476f6d8241e603fc962e7fd3d2.jpg",
        "d_starring": null,
        "d_tag": null,
        "d_remarks": "TC",
        "d_area": null,
        "d_lang": null,
        "d_year": null,
        "d_type": "10",
        "d_level": null,
        "d_hits": 0,
        "d_score": "7.9",
        "d_time": null,
        "d_content": null,
        "d_playurl": null,
        "d_downurl": null,
        "isStore": 0
      },
      {
        "d_id": 70012,
        "d_name": "坚如磐石",
        "d_ldgletter": null,
        "d_enname": null,
        "d_pic": "http://img.lzzyimg.com/upload/vod/20231002-1/f2990fb78572fea4643d058f4c2850ce.jpg",
        "d_starring": null,
        "d_tag": null,
        "d_remarks": "HD",
        "d_area": null,
        "d_lang": null,
        "d_year": null,
        "d_type": "5",
        "d_level": null,
        "d_hits": 0,
        "d_score": "6.5",
        "d_time": null,
        "d_content": null,
        "d_playurl": null,
        "d_downurl": null,
        "isStore": 0
      },
      {
        "d_id": 72940,
        "d_name": "惊奇队长2",
        "d_ldgletter": null,
        "d_enname": null,
        "d_pic": "http://img.lzzyimg.com/upload/vod/20231113-1/0aeaad64e80bf051de7878d48b4f39d0.jpg",
        "d_starring": null,
        "d_tag": null,
        "d_remarks": "HD",
        "d_area": null,
        "d_lang": null,
        "d_year": null,
        "d_type": "5",
        "d_level": null,
        "d_hits": 0,
        "d_score": "5.4",
        "d_time": null,
        "d_content": null,
        "d_playurl": null,
        "d_downurl": null,
        "isStore": 0
      },
      {
        "d_id": 70490,
        "d_name": "前任4：英年早婚",
        "d_ldgletter": null,
        "d_enname": null,
        "d_pic": "http://img.lzzyimg.com/upload/vod/20231008-1/a631605017b6c84c1bcd26a9a4cff174.jpg",
        "d_starring": null,
        "d_tag": null,
        "d_remarks": "HD",
        "d_area": null,
        "d_lang": null,
        "d_year": null,
        "d_type": "6",
        "d_level": null,
        "d_hits": 0,
        "d_score": "6.1",
        "d_time": null,
        "d_content": null,
        "d_playurl": null,
        "d_downurl": null,
        "isStore": 0
      },
      {
        "d_id": 74322,
        "d_name": "长安诡事传",
        "d_ldgletter": null,
        "d_enname": null,
        "d_pic": "http://img.lzzyimg.com/upload/vod/20231128-1/b23dcba9d6ef45f088b7ed122eb653d9.jpg",
        "d_starring": null,
        "d_tag": null,
        "d_remarks": "HD",
        "d_area": null,
        "d_lang": null,
        "d_year": null,
        "d_type": "10",
        "d_level": null,
        "d_hits": 0,
        "d_score": "0.0",
        "d_time": null,
        "d_content": null,
        "d_playurl": null,
        "d_downurl": null,
        "isStore": 0
      },
      {
        "d_id": 64405,
        "d_name": "碟中谍7：致命清算[上]",
        "d_ldgletter": null,
        "d_enname": null,
        "d_pic": "http://pic.lzzypic.com/upload/vod/20230718-1/b1baed95726db96749476dc7ae92174e.jpg",
        "d_starring": null,
        "d_tag": null,
        "d_remarks": "HD",
        "d_area": null,
        "d_lang": null,
        "d_year": null,
        "d_type": "5",
        "d_level": null,
        "d_hits": 0,
        "d_score": "7.9",
        "d_time": null,
        "d_content": null,
        "d_playurl": null,
        "d_downurl": null,
        "isStore": 0
      },
      {
        "d_id": 72329,
        "d_name": "第八个嫌疑人",
        "d_ldgletter": null,
        "d_enname": null,
        "d_pic": "http://img.lzzyimg.com/upload/vod/20231103-1/1d98a14b36d7873469b5feee5e1303b6.jpg",
        "d_starring": null,
        "d_tag": null,
        "d_remarks": "HD",
        "d_area": null,
        "d_lang": null,
        "d_year": null,
        "d_type": "10",
        "d_level": null,
        "d_hits": 0,
        "d_score": "6.2",
        "d_time": null,
        "d_content": null,
        "d_playurl": null,
        "d_downurl": null,
        "isStore": 0
      },
      {
        "d_id": 70676,
        "d_name": "电锯惊魂10",
        "d_ldgletter": null,
        "d_enname": null,
        "d_pic": "http://img.lzzyimg.com/upload/vod/20231011-1/7fd3c32319dc3a59e4c4e49e4cb559c0.jpg",
        "d_starring": null,
        "d_tag": null,
        "d_remarks": "HD",
        "d_area": null,
        "d_lang": null,
        "d_year": null,
        "d_type": "9",
        "d_level": null,
        "d_hits": 0,
        "d_score": "7.7",
        "d_time": null,
        "d_content": null,
        "d_playurl": null,
        "d_downurl": null,
        "isStore": 0
      },
      {
        "d_id": 70847,
        "d_name": "学爸",
        "d_ldgletter": null,
        "d_enname": null,
        "d_pic": "http://img.lzzyimg.com/upload/vod/20231013-1/1075231ed6cd8f9541b1f44c8f43f9ab.jpg",
        "d_starring": null,
        "d_tag": null,
        "d_remarks": "HD",
        "d_area": null,
        "d_lang": null,
        "d_year": null,
        "d_type": "6",
        "d_level": null,
        "d_hits": 0,
        "d_score": "6.6",
        "d_time": null,
        "d_content": null,
        "d_playurl": null,
        "d_downurl": null,
        "isStore": 0
      },
      {
        "d_id": 64626,
        "d_name": "长安三万里",
        "d_ldgletter": null,
        "d_enname": null,
        "d_pic": "http://pic.lzzypic.com/upload/vod/20230720-1/6601f6e0a34e63aa9c11a101a41004ac.jpg",
        "d_starring": null,
        "d_tag": null,
        "d_remarks": "HD",
        "d_area": null,
        "d_lang": null,
        "d_year": null,
        "d_type": "25",
        "d_level": null,
        "d_hits": 0,
        "d_score": "8.2",
        "d_time": null,
        "d_content": null,
        "d_playurl": null,
        "d_downurl": null,
        "isStore": 0
      },
      {
        "d_id": 64970,
        "d_name": "封神第一部：朝歌风云",
        "d_ldgletter": null,
        "d_enname": null,
        "d_pic": "http://pic.lzzypic.com/upload/vod/20230726-1/c800ed50a9df9142fc4c5a0f428fbfb3.jpg",
        "d_starring": null,
        "d_tag": null,
        "d_remarks": "HD",
        "d_area": null,
        "d_lang": null,
        "d_year": null,
        "d_type": "5",
        "d_level": null,
        "d_hits": 0,
        "d_score": "7.7",
        "d_time": null,
        "d_content": null,
        "d_playurl": null,
        "d_downurl": null,
        "isStore": 0
      },
      {
        "d_id": 64905,
        "d_name": "茶啊二中",
        "d_ldgletter": null,
        "d_enname": null,
        "d_pic": "http://pic.lzzypic.com/upload/vod/20230725-1/99ae2b7e8fd4e34bb284908dec9e5533.jpg",
        "d_starring": null,
        "d_tag": null,
        "d_remarks": "HD",
        "d_area": null,
        "d_lang": null,
        "d_year": null,
        "d_type": "6",
        "d_level": null,
        "d_hits": 0,
        "d_score": "7.8",
        "d_time": null,
        "d_content": null,
        "d_playurl": null,
        "d_downurl": null,
        "isStore": 0
      },
      {
        "d_id": 68820,
        "d_name": "暗杀风暴",
        "d_ldgletter": null,
        "d_enname": null,
        "d_pic": "http://img.lzzyimg.com/upload/vod/20230916-1/74512f53f800a5b011ccda290a6af209.jpg",
        "d_starring": null,
        "d_tag": null,
        "d_remarks": "HD",
        "d_area": null,
        "d_lang": null,
        "d_year": null,
        "d_type": "10",
        "d_level": null,
        "d_hits": 0,
        "d_score": "6.1",
        "d_time": null,
        "d_content": null,
        "d_playurl": null,
        "d_downurl": null,
        "isStore": 0
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
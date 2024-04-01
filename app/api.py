from flask import Blueprint


bp = Blueprint('api',__name__, url_prefix='/api')


@bp.route("/hot_video_list")
def api_hot_video_list():
    json = """
    {
    "code": 0,
    "data": [
        {
		        "id" : "111111"
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

@bp.route("search",methods=['GET','POST'])
def api_search():
    json = """
{
    "code": 0,
    "data": [
        {
		        "id" : "111111"
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
    ],
     "page_info": {
		    "page_no": 2,
		    "page_size": 10,
			  "page_total": 13,
     }
}
"""
    return json

@bp.route("video_info",methods=['GET','POST'])
def api_video_info():
    json = """
    {
    "code": 0,
    "data": {
		        "id" : "111111"
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
}
"""
    return json

@bp.route("video_play_urls",methods=['GET','POST'])
def api_video_play_urls():
    json = """
        {
            "code": 0,
            "data": [
                {
                    "第01集": "https://v.cdnlz9.com/share/308a4f1079d3c50653dfeca80d85ea6a"
                },
                {
                    "第02集": "https://v.cdnlz9.com/share/308a4f1079d3c50653dfeca80d85ea6a"
                }
            ],
            "page_info": {
                    "page_no": 2,
                    "page_size": 10,
                    "page_total": 13,
            }
        }
"""
    return json
import requests
from app.services import DoubanService




if __name__ == "__main__":
    # url = "http://127.0.0.1:5000/api/search"
    # r = requests.post(url,data={"region":"日本","page_no":1})
    # print(r.text)


    url = "http://127.0.0.1:5000/api/hot_video_list"
    r = requests.post(url,data={"type":"movie"})
    print(r.text)


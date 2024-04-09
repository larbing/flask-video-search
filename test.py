import requests




if __name__ == "__main__":
    url = "http://127.0.0.1:5000/api/video_play_urls"
    r = requests.post(url,data={"id":"512168fde4ac3c38eedfc9a42eeef3e4","page_no":"3"})
    print(r.text)
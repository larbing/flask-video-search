import requests




if __name__ == "__main__":
    url = "http://127.0.0.1:5000/api/search"
    r = requests.post(url,data={"region":"日本","name":"小红帽恰恰","page_no":1})
    print(r.text)
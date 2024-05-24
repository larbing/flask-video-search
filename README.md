# flask-video-search


### 接口文档地址 https://cactus-buzzard-dbd.notion.site/18e982bfabd74fd4bcb082e14c9144cb

## docker运行

~~~
先下载解压数据包到 /data 目录下

docker run -d --rm -p 80:80 \
            -v /data:/data \
            --name {IMAGE_NAME} \
            {USER_NAME}/{IMAGE_NAME}"
~~~

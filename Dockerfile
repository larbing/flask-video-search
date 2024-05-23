FROM python:3

WORKDIR /home/app

COPY requirements.txt ./

RUN pip install -i https://mirrors.aliyun.com/pypi/simple/  pip -U
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ 

# RUN mkdir -p /data/app/indexdir
# RUN touch /data/app/db.json
ENV TZ 'Asia/Shanghai'

COPY . .

CMD [ "python", "./run.py" ]
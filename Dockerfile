FROM python:3

WORKDIR /home/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

# RUN mkdir -p /data/app/indexdir
# RUN touch /data/app/db.json

COPY . .

CMD [ "python", "./run.py" ]
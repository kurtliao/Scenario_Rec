FROM python:2
MAINTAINER Kurt Liao <akurtliao@gmail.com>
COPY . /src
WORKDIR /src
RUN pip install -r requirements.txt
EXPOSE 80
CMD sleep 10 && python Insert_Json_DB.py && python demo3_server_v1.py

#docker run -itd --name postgres -e POSTGRES_PASSWORD=demois1207 -d postgres
#docker run --name redis -d redis
#docker build -t tag_api:3.0 .
#docker run -itd --name scenario_rec3 -p 6030:6030 --link redis:redis --link postgres:postgres tag_api:3.0

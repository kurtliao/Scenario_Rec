FROM python:2
MAINTAINER Kurtliao <akurtliao@gmail.com>
COPY . /src
WORKDIR /src
EXPOSE 80
RUN pip install -r requirements.txt
CMD sleep 10 && python demo3_server_v1.py
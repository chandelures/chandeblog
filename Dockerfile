FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /chandeblog
WORKDIR /chandeblog

ADD requirements.txt /chandeblog/
ADD bower.json /chandeblog/
ADD .bowerrc /chandeblog/

RUN apt install bower -y \
 && bower install \
 && pip install pip -U -i https://pypi.tuna.tsinghua.edu.cn/simple \
 && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ADD . /chandeblog/

FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /chandeblog
WORKDIR /chandeblog

ADD requirements.txt /chandelure/

RUN pip install pip -U -i https://pypi.tuna.tsinghua.edu.cn/simple \
 && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ADD . /chandeblog/

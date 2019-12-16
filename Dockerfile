FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /chandeblog
WORKDIR /chandelure

ADD requirements.txt /chandelure/

RUN pip install pip -U -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ADD . /code/

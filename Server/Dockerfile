FROM python:3.10.10

ENV PYTHONUNBUFFERED 1

RUN mkdir /Server

WORKDIR /Server

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip config set install.trusted-host https://pypi.tuna.tsinghua.edu.cn

RUN python -m pip install -U pip

#RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list
#RUN sed -i s@/security.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list
#RUN apt update -y


CMD pip install -r requirements.txt && python manage.py makemigrations && python manage.py migrate && gunicorn -c gunicorn.conf.py Server.asgi:application

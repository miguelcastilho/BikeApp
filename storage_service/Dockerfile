FROM python:2.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV http_proxy http://proxy.sdc.hp.com:8080/
ENV https_proxy http://proxy.sdc.hp.com:8080/

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

CMD python /usr/src/app/app.py

ENV http_proxy ""
ENV https_proxy ""

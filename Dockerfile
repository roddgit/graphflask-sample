FROM python:3.9-slim

ENV http_proxy http://192.168.45.105:8080
ENV https_proxy http://192.168.45.105:8080
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get -y install apt-utils \
    && apt-get -y install unzip \
    && apt-get -y install git \
    && apt-get -y install nano \
    && apt-get install tzdata -y \
    && mkdir -p /logs

RUN chmod -R 777 /logs/

ENV TZ=Asia/Jakarta
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip --proxy=http://192.168.45.105:8080 install -r requirements.txt
COPY . /app
EXPOSE 5000

CMD ["python", "app.py"]
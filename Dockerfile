FROM python:3.10.0-alpine

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apk add --no-cache python3-dev libstdc++ && \
    apk add --no-cache g++ && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /app

EXPOSE 8000
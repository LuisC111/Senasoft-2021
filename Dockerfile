FROM ubuntu

RUN apt install python3-dev \
    && pip3 install --upgrade pip

WORKDIR /app

COPY . /app

RUN bash start.sh
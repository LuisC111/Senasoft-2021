FROM alpine:3.13.6

RUN apk add --no-cache python3-dev \
    && apk add mariadb-connector-c-dev \
    && apk add gcc \
    && apk add g++ \
    && apk add postgresql-dev gcc \
    && apk add py3-pip \
    && pip3 install --upgrade pip 

WORKDIR /app

COPY . /app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip3 install --upgrade pip 
RUN pip3 --no-cache-dir install -r requirements.txt

CMD [ "python3", "main.py" ]
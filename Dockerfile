FROM arm32v7/python:alpine

WORKDIR /unipi
COPY requirements.txt coinslot.py ./
RUN apk add --no-cache --virtual .build-deps build-base \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

ENTRYPOINT [ "python", "./coinslot.py" ]

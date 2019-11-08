FROM python:3.7.3-buster

RUN apt-get update && apt-get install build-essential
WORKDIR /unipi
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python3", "./unipi-coinslot" ]
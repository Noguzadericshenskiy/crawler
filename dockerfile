FROM python:3.8

RUN python -m pip install --upgrade pip
WORKDIR /app

COPY crawler_1.py /app/
COPY crawler_2.py /app/
COPY requirements.txt /app/

RUN pip install -r /app/requirements.txt

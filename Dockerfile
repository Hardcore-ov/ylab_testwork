FROM python:3.10.5

WORKDIR .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .
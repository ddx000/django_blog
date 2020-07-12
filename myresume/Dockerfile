# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /home/web

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirement.txt .

# install pillow dependencies
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers \
    && pip install Pillow

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip && \ 
 pip install --no-cache-dir -r requirement.txt

# copy project
COPY . .

ENTRYPOINT ["/home/web/entrypoint.sh"]

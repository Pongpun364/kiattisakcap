# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/firstweb

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

RUN apk update &&\
    apk add --no-cache --virtual .tmp-deps \
    # dependency for pillow
    gcc libc-dev linux-headers zlib-dev jpeg-dev\
    # dependency for postgresql
    python3-dev musl-dev postgresql-dev &&\
    # permanent dependency
    apk add --no-cache libpq libjpeg libffi-dev openssl-dev &&\
    pip install --upgrade pip &&\
    pip install -r requirements.txt &&\
    # deletine the virtual dependency
    apk del --no-cache .tmp-deps


# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/firstweb/entrypoint.sh
RUN chmod +x /usr/src/firstweb/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/firstweb/entrypoint.sh"]
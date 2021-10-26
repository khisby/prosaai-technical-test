FROM python:3.7-stretch

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Jakarta
RUN apt-get install -y tzdata

COPY backend/requirements.txt /

RUN pip install --upgrade pip

RUN pip install -r /requirements.txt

COPY backend /app

WORKDIR /app

CMD [ "python", "/app/chat.py" ]



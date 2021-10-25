FROM python:3.7-stretch

COPY backend/requirements.txt /

RUN pip install --upgrade pip

RUN pip install -r /requirements.txt

COPY backend /app

WORKDIR /app

CMD [ "python", "/app/chat.py" ]



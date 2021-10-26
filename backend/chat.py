#!/bin/env python
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import uuid
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from requests import get
import os
import logging
from logging import Formatter, FileHandler




socketio = SocketIO()
token = "2094159366:AAHtSL81Jj95zzwWWHLe6AzrLJvpfjGWyh4"
url = f'https://api.telegram.org/bot{token}/'


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'khisoft#'

socketio.init_app(app)

df = pd.read_csv('dialogs.txt', header=None, delimiter='\t')
vec = TfidfVectorizer(lowercase=True)
X = vec.fit_transform(df[0])
questions = X.toarray()

@app.route('/')
def chat():
    list_question = df[0].values
    session['id'] = uuid.uuid4()
    return render_template('chat.html', id=id, list_question=list_question)

@app.route('/telegram',methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        app.logger.debug('Pesan {}'.format(data)) 
        if '/start' in str(data):
            id   = data['message']['chat']['id']
            nama  = data['message']['chat']['first_name']
            teks      = f'Hallo {nama} !\nKhisoftBot in here, welcome. !\nAsk me a question. '
            sendMessage(id,teks)
        else:
            id = data['message']['chat']['id']
            message = data['message']['text']
            (answer, score, question) = getAnswer(message)

            if(score > 0.1):
                    sendMessage(id,answer)
            else:
                    sendMessage(id,"I'am sorry. I don't understand")
        return 'received'
    else:
        return "Hallo ini bot telegram"

def sendMessage(id,teks):
    data = {
        'chat_id':id,
        'text':teks
    }
    get(url+'sendMessage',params=data)


@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    join_room(room)

@socketio.on('text', namespace='/chat')
def text(message):
        room = session.get('room')
        message = message["msg"].lower()
        (answer, score, question) = getAnswer(message)

        if(score > 0.1):
                emit('message', {'msg': answer}, room=room)
        else:
                emit('message', {'msg': "I'am sorry. I don't understand"}, room=room)

@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    leave_room(room)

def getAnswer(msg):
    text_vec = vec.transform([msg])
    text_vec = text_vec.toarray()
    text_vec = text_vec[0].reshape(1, -1) 
    similarity = cosine_similarity(text_vec, questions)
    answer_index = np.argmax(similarity[0])
    answer = df[1].iloc[answer_index]
    question = df[0].iloc[answer_index]
    return answer, similarity[0][answer_index], question

if __name__ == '__main__':
    file_handler = FileHandler('app.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s : %(message)s'))
    app.logger.addHandler(file_handler)
    socketio.run(app, port=5000, host="0.0.0.0")

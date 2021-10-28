import json
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from flask import Flask, render_template, request, jsonify, Response, send_from_directory
import random
import pickle

with open("intents.json", encoding='utf-8') as file:
    data = json.load(file)

model = keras.models.load_model('chat_model')

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

with open('label_encoder.pickle', 'rb') as enc:
    lbl_encoder = pickle.load(enc)

max_len = 20


app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    try:
        mes = request.form['mes']
        print(mes)
        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([mes]),
                                                                          truncating='post', maxlen=max_len))

        tag = lbl_encoder.inverse_transform([np.argmax(result)])

        for i in data['intents']:
            if i['tag'] == tag:
                if tag == 'film':
                    film = np.random.choice(i['responses'])
                    print(np.random.choice(i['responses']))
                    return jsonify({'ans': film['param1'] + "<br />" + film['param2'] + "<br />" + "<a href=\"" + film['param3'] + "\">Ссылка</a>" + "<br />" + "<img src=\"" + film['param4'] + "\">"})
                else:
                    print(np.random.choice(i['responses']))
                    return jsonify({'ans': np.random.choice(i['responses'])})

    except Exception as ex:
        return jsonify({'error': str(ex)})


if __name__ == "__main__":
    app.run()

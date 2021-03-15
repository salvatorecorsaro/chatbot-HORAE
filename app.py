from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS

import json
import numpy as np
from tensorflow import keras


import pickle

with open("intents.json") as file:
    data = json.load(file)

app = Flask(__name__)
CORS(app)
api = Api(app)


class ChatBot(Resource):
    def get(self, message):
        return{"data": "" + chat(message)}


api.add_resource(ChatBot, "/chat-bot/<string:message>")


def chat(message):
    # load trained model
    model = keras.models.load_model('chat_model')

    # load tokenizer object
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    # parameters
    max_len = 20

    inp = message

    result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                                                      truncating='post', maxlen=max_len))
    tag = lbl_encoder.inverse_transform([np.argmax(result)])

    for i in data['intents']:
        if i['tag'] == tag:
            return np.random.choice(i['responses'])




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)




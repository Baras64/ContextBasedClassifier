import pandas as pd
from flask import Flask, jsonify, request
import tensorflow as tf
import unicodedata
import re
import pickle,joblib

# load model
tokenizer = joblib.load(r'C:\Users\Harsh\Desktop\AmazonProjects\TsecHacks\Newtokenizer.pickle')
model = tf.keras.models.load_model(r'C:\Users\Harsh\Desktop\AmazonProjects\TsecHacks\Model.h5')

# app
app = Flask(__name__)

# routes
@app.route('/', methods=['POST'])

def predict(text):

    def unicode_to_ascii(s):
        return ''.join(c for c in unicodedata.normalize('NFD', s)
                       if unicodedata.category(c) != 'Mn')

    def preprocess(w):
        w = unicode_to_ascii(w.lower().strip())
        w = re.sub(r"([?.!,¿])", r" \1 ", w)
        w = re.sub(r'[" "]+', " ", w)
        w = re.sub(r"newlinechar", "", w)
        w = re.sub(r"[^a-zA-Z?.!,¿]+", " ", w)
        w = w.rstrip().strip()

        return w


    def hax(sentence):
        sentence = preprocess(sentence)
        sentence = tokenizer.texts_to_sequences([sentence])
        padded = tf.keras.preprocessing.sequence.pad_sequences(sentence, maxlen=25, padding='post', truncating='pre')
        return padded
    # get data
    data = request.get_json(force=True)

    # predictions
    result = model.predict(hax(text))

    # send back to browser
    output = {'results': int(result[0])}

    # return data
    return jsonify(results=output)

if __name__ == '__main__':
    app.run(port = 5000, debug=True)
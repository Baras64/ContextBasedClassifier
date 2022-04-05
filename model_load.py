import h5py
import tensorflow as tf
import joblib
import unicodedata
import re

api = ""

class Model():
    def __init__(self):
        self.model = tf.keras.models.load_model(r"C:\Users\HARSHAVARDHAN A\PycharmProjects\TsecHacks\Model.h5")
        self.tokenizer = joblib.load(r"C:\Users\HARSHAVARDHAN A\PycharmProjects\TsecHacks\Newtokenizer.pickle")

    def unicode_to_ascii(self, s):
        return ''.join(c for c in unicodedata.normalize('NFD', s)
                       if unicodedata.category(c) != 'Mn')

    def preprocess(self, w):
        w = self.unicode_to_ascii(w.lower().strip())
        w = re.sub(r"([?.!,¿])", r" \1 ", w)
        w = re.sub(r'[" "]+', " ", w)
        w = re.sub(r"newlinechar", "", w)
        w = re.sub(r"[^a-zA-Z?.!,¿]+", " ", w)
        w = w.rstrip().strip()
        # w = w.replace('.', '')
        print(w)

        return w

    def filter(self, sentence):
        sentence = self.preprocess(sentence)
        sentence = self.tokenizer.texts_to_sequences([sentence])
        padded = tf.keras.preprocessing.sequence.pad_sequences(sentence, maxlen=10, padding='post', truncating='pre')#previous 25
        return padded

    def predicton(self, text):
        return self.model.predict(self.filter(text))

if __name__ == "__main__":
    obj = Model()
    obj.predicton('This is not an if else statement')

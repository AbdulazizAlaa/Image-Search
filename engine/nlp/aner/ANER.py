import fasttext
from keras.models import model_from_json
import pandas as pd
import numpy as np
from keras import backend as K


class ANER(object):
    def solve(self, text):
        """This is where the magic happens."""
        result = self.sentence2sequence(text)
        result = result[(self.seq_length - len(text.split(" "))):]
        tags = []
        print(result)
        for idx, item in zip(range(len(result)), result):
            if(item == "B-PERS" or item == "I-PERS"):
                print(item)
                tags.append(text.split(" ")[idx])
        return tags


    def preprocess(self, text):
        pass
    
    def __init__(self):
        K.set_learning_phase(1)
        with open("engine/nlp/aner/model.json", "r") as lstm_string:
            self.lstm = model_from_json(lstm_string.read())
        self.lstm.load_weights("engine/nlp/aner/weights.hdf")
        self.vecs = fasttext.load_model("engine/nlp/aner/wiki.ar.bin")
        classes = pd.read_csv("engine/nlp/aner/classes.csv", header=None)
        self.classes = classes[1].tolist()
        self.seq_length = 10

    def sentence2sequence(self, sentence):
        tokens = sentence.split(" ")
        model = self.lstm
        vec_model = self.vecs
        classes = self.classes
        seq_length = self.seq_length

        sentence_vec = [vec_model[token] for token in tokens]
        sentence_length = len(sentence_vec)
        for i in range(seq_length - sentence_length):
            sentence_vec = np.concatenate((np.zeros((1, 300)), sentence_vec), axis=0)
        sentence_vec = sentence_vec.reshape((1, 10, 300))
        predictions = model.predict_classes(sentence_vec)[0]
        predictions = [classes[item] for item in predictions]
        return predictions

from distutils.command import clean
import json
import os
import random
import json
import pickle
from django.conf import settings
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open(os.path.join(settings.BASE_DIR, "model/intents.json")).read())
words = pickle.load(open(os.path.join(settings.BASE_DIR, "model/words.pkl"), "rb"))
classes = pickle.load(open(os.path.join(settings.BASE_DIR, "model/classes.pkl"), "rb"))

model = load_model(os.path.join(settings.BASE_DIR, "model/chatbot_model.h5"))


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bag = bag_of_words(sentence)
    res = model.predict(np.array([bag]))[0]
    results = [[i, r] for i, r in enumerate(res)]
    print(results)
    if results:
        results.sort(key=lambda x: x[1], reverse=True)
        return classes[results[0][0]]
    else:
        return ""


def get_response(intent, intents_json):
    if intent == "":
        return "Sorry I cant answer that."
    tag = intent
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            return random.choice(i["responses"])


if __name__ == "__main__":
    print("GO! Bot is running!")
    while True:
        user_input = input("You: ")
        if user_input == "quit":
            break
        result = predict_class(user_input)
        print("Bot: ", get_response(result, intents))

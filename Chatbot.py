#import necessary modules

import nltk
import io
import numpy as np
import random
import string
import warnings
import os
import speech_recognition as sr
from playsound import playsound
from gtts import gTTS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
warnings.filterwarnings("ignore")

#News Database
f = open('details.txt')
raw = f.read().lower()
nltk.download("punkt")
nltk.download("wordnet")
sent_tokens = nltk.sent_tokenize(raw) #Puts each sentence of paragraph into a list/array
word_tokens = nltk.word_tokenize(raw) #Puts each word of a sentence into a list/array

#Pre-Processing
lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct)))



#Greeting database
USER_GREETINGS = ('hello', 'hi', 'hey', 'greetings', 'good morning')
BOT_GREETINGS = ["hi", "hey", "hello", "nice to meet you", "hi what's up"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in USER_GREETINGS:
            return random.choice(BOT_GREETINGS)

#Response system
def respond(user_input):
    chatbot_response = ''
    sent_tokens.append(user_input)
    Vec = TfidfVectorizer(tokenizer=LemNormalize, stop_words="english")
    tfidf = Vec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if req_tfidf == 0:
        chatbot_response = chatbot_response + """Sorry I don't understand"""
        return chatbot_response
    else:
        chatbot_response = chatbot_response + sent_tokens[idx]
        return chatbot_response
    
#Input from mic here


#Program

def recenews(user_input):
        if user_input != "bye":
            if user_input == "thanks" or user_input == "thank you":
                running = False
                return """Bot: You're welcome"""
            
            else:
                if greeting(user_input) != None:
                    return "Chatbot: "+ greeting(user_input)
                else:
                    print("Chatbot: ", end="")
                    res = respond(user_input)
                    sent_tokens.remove(user_input)
                    return res
        else:
            running = False
            print("Chatbot: Bye, have a nice day.")
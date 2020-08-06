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

#Text to speech will go here


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

running = True
print(hello)
voice_or_text = input("""Push '1' to enter in text or '2' to use speech: """)

reports = list()

while running:
    print("")
    print(push_one)
    playsound("push_one.mp3")
    print(push_two)
    playsound("push_two.mp3")
    print(push_three)
    playsound("push_three.mp3")
    
    if voice_or_text == '2':
        user_input = str()
        get_audio()
        user_input = user_input.lower()
    elif voice_or_text == '1':
        user_input = input().lower()
        
    if user_input != "bye":
        if user_input == "thanks" or user_input == "thank you":
            running = False
            print("""Bot: You're welcome""")
            
        elif user_input == "1" or user_input == "report":
            playsound("issue.mp3")
            myreport = input("Please describe the issue: ")
            reports.append(myreport)
            print("Thank you for the feedback. The authorities will be informed that: %s and will be acted upon" %myreport)
        elif user_input == "2" or user_input == "info":
            playsound("askany.mp3")
            question = input("Please ask anything about the camp: ").lower()
            if greeting(question) != None:
                print("Chatbot: "+ greeting(user_input))
            else:
                print("Chatbot: ", end="")
                print(respond(question))
                sent_tokens.remove(question)
        elif user_input == "3" or user_input == "survey":
            print("Work in Progress")
        else:
            if greeting(user_input) != None:
                print("Chatbot: "+ greeting(user_input))
            else:
                print("Chatbot: ", end="")
                print(respond(user_input))
                sent_tokens.remove(user_input)
    else:
        running = False
        print("Chatbot: Bye, have a nice day.")
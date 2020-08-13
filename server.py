from flask import Flask
from flask import render_template, request, redirect
from playsound import playsound
from gtts import gTTS
import Chatbot
import os
app = Flask(__name__)

voice = True

@app.route('/')
def landing():
    sound = "static/welcome_audio.mp3"
    return render_template('index.html', sound=sound, voice=voice)

@app.route('/home')
def home():
    sound = "static/pronewsur.mp3"
    return render_template('home.html', sound=sound, voice=voice)

@app.route('/news')
def news():
    if voice == True:
        pass
    return render_template("news.html", sound=sound, voice=voice)

@app.route('/report')
def report():
    return render_template('report.html', sound=sound, voice=voice)

@app.route('/survey')
def survey():
    if voice == True:
        pass
    return render_template('survey.html', sound=sound, voice=voice)

@app.route('/vot')
def vot():
    sound = "static/voice_or_text.mp3"
    return render_template('vot.html', sound=sound, voice=voice)

@app.route("/home-query")
def home_query():
    answer = request.args.get('todo') 
    if answer == "1":
        return redirect("/report")
    elif answer == "2":
        return redirect("/news")
    elif answer == "3":
        return redirect("/survey")

@app.route('/language-query')
def language_query():
    answer = request.args.get('ling')
    if answer == "1":
        return redirect("/vot")
    return "Not Understood"

@app.route('/news-query')
def news_query():
    answer = request.args.get('news')
    info = Chatbot.recenews(answer)
    if voice == True:
        tts = gTTS(text=info)
        tts.save("news_answer.mp3")
        playsound("news_answer.mp3")
        os.remove("news_answer.mp3")
    return render_template("news.html", message=info)

@app.route('/vot-query')
def vot_query():
    global voice
    voice = True
    answer = request.args.get('vot')
    if answer == "1":
        return redirect("/home")
    elif answer == "2":
        voice = False
        return redirect("/home")
    else:
        return "Sorry I don't understand"

@app.route('/report-query')
def report_query():
    # WARNING: NOT SECURE!!!
    answer = request.args.get('answer')
    speak = 'Thank you for your report that ' +answer
    if voice == True:
        tts = gTTS(speak)
        tts.save("report.mp3")
        playsound("report.mp3")
        os.remove("report.mp3")
    return f'Thank you for your report that "{answer}"'

@app.route('/survey-query')
def survey_query():
    # WARNING: NOT SECURE!!!
    return redirect("/home")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
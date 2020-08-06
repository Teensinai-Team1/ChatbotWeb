from flask import Flask
from flask import render_template, request, redirect
from playsound import playsound
from gtts import gTTS
app = Flask(__name__)

voice = False

@app.route('/')
def landing():
    playsound("Welcome.mp3")
    playsound("lang_query.mp3")
    playsound("one_en.mp3")
    #playsound("two_swa.mp3")
    return render_template('index.html')

@app.route('/home')
def home():
    playsound("action_query.mp3")
    playsound("one_prob.mp3")
    playsound("two_news.mp3")
    playsound("three_survey.mp3")
    return render_template('home.html')

@app.route('/news')
def news():
    return "I Don't have any news yet"

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/survey')
def survey():
    return render_template('survey.html')

@app.route('/vot')
def vot():
    playsound("method_query.mp3")
    playsound("one_voice.mp3")
    playsound("two_text.mp3")
    return render_template('vot.html')

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


@app.route('/vot-query')
def vot_query():
    answer = request.args.get('vot')
    if answer == "1":
        return "W.I.P"
    elif answer == "2":
        return redirect("/home")
    else:
        return "Sorry I don't understand"

@app.route('/report-query')
def report_query():
    # WARNING: NOT SECURE!!!
    answer = request.args.get('answer')
    return f'thank you for your report that "{answer}"'

@app.route('/survey-query')
def survey_query():
    # WARNING: NOT SECURE!!!
    answer1 = request.args.get('answer1')
    answer2 = request.args.get('answer2')
    return f'you submitted "{answer1}" in response to the first question \
             and "{answer2}" in response to the second question.'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
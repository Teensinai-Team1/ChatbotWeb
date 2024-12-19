from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from playsound import playsound
from gtts import gTTS
import Chatbot
import os

base_directory = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fourwordsalluppercase!'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///'+ os.path.join(base_directory, 'database.db')
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'forms'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

def login_authentication_thingy(form):
   user = User.query.filter_by(username=form.username.data).first()
   if user:
        if check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        return '<h1>Invalid username or password</h1>'

voice = True

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/community')
def comm():
  return render_template('comm.html')

@app.route('/forms', methods=["POST", "GET"])
def forms():
  logging = LoginForm()
  signing = RegisterForm()
  
  if request.method == "GET":
      return render_template('forms.html', logging=logging, signing=signing)

  action = request.form.get("authenticate")

  if action == "register":
    if signing.validate_on_submit():
        duplicate_user = User.query.filter_by(username=signing.username.data).first()
        if not duplicate_user:
            hashed_password = generate_password_hash(signing.password.data, method='pbkdf2:sha256')
            new_user = User(username=signing.username.data, email=signing.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return login_authentication_thingy(signing)
        flash("Username already exists", category="failure")
        return render_template('forms.html', logging=logging, signing=signing)
            

  elif action == "login":
    if logging.validate_on_submit():
        return login_authentication_thingy(logging)

    return render_template('forms.html', logging=logging, signing=signing)



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



@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('forms'))

@app.route('/chat')
def chat():
    if 'message' in request.args:
        message = request.args['message']

        return Chatbot.message(message)
    else:
        return "Error: No message."

@app.route('/summary')
def summary():
    
    return Chatbot.summary()


if __name__ == '__main__':
  app.debug = True
  app.run( # Starts the site
		host='0.0.0.0',  
		port=8000
	)
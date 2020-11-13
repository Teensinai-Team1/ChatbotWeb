from flask import Flask
from flask import render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fourwordsalluppercase!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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
    #email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])



voice = True

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/community')
def comm():
  return render_template('comm.html')

@app.route('/forms')
def forms():
  logging = LoginForm()
  signing = RegisterForm()

  return render_template('forms.html', logging=logging, signing=signing)

@app.route('/login-query', methods=['GET', 'POST'])
def login_query():

  if logging.validate_on_submit():
      user = User.query.filter_by(username=form.username.data).first()
      if user:
          if check_password_hash(user.password, form.password.data):
              login_user(user, remember=form.remember.data)
              return redirect(url_for('dashboard'))

      return '<h1>Invalid username or password</h1>'

  return redirect(url_for("user"))

@app.route('/signup-query', methods=['GET', 'POST'])
def signup():
  if signing.validate_on_submit():
      hashed_password = generate_password_hash(signing.password.data, method='sha256')
      new_user = User(username=signing.username.data, email=signing.email.data, password=hashed_password)
      db.session.add(new_user)
      db.session.commit()

      return '<h1>New user has been created!</h1>'

  return redirect(url_for("forms"))



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
#@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
  app.debug = True
  app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)
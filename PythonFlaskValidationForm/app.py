from tokenize import String
from flask import Flask, render_template
from flask_wtf import FlaskForm

# potrzebujemy do wykonania formularza pole tekstowe i pole dla hasla
from wtforms import StringField, PasswordField

# podanie sciezki do template'ow HTML
app = Flask(__name__, template_folder='templates')

# secret key
app.config['SECRET_KEY'] = 'Thisisasecret!'

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')

# Route do strony glownej
@app.route('/')
def home():
    return render_template('home.html')

# Route do przykladowego formularza
@app.route('/form')
def form():
    form = LoginForm()
    return render_template('form.html', form=form)

# Tymczasowy run dla debugu z przegladarki - ustawic pozniej np. na localhost:80
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
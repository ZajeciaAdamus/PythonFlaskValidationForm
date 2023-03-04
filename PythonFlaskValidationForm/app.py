from tokenize import String
from flask import Flask, render_template
from flask_wtf import FlaskForm

# potrzebujemy do wykonania formularza pole tekstowe i pole dla hasla
from wtforms import StringField, PasswordField

# podanie sciezki do template'ow HTML
app = Flask(__name__, template_folder='templates')

# secret key
app.config['SECRET_KEY'] = 'Thisisasecret!'

class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')

# Route do strony glownej
@app.route('/')
def home():
    return render_template('home.html')

# Route do przykladowego formularza
@app.route('/form', methods=['GET','POST'])
def form():
    form = LoginForm()
    if form.validate_on_submit(): #jesli formularz zostal wyslany, to zwracamy info
        return 'Formularz zostal wyslany!'
    return render_template('form.html', form=form)

# Tymczasowy run dla debugu z przegladarki - ustawic pozniej np. na localhost:80
if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template
from flask_wtf import FlaskForm
# potrzebujemy do wykonania formularza pole tekstowe i pole dla hasla
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, AnyOf

# podanie sciezki do template'ow HTML
app = Flask(__name__, template_folder='templates')

# secret key
app.config['SECRET_KEY'] = 'Thisisasecret!'

class LoginForm(FlaskForm):
    username = StringField('username',
                             validators=[InputRequired('Username is required'),
                             Length(min=5,max=10, message='Type 5 to 10 characters.')])
    password = PasswordField('password',
                             validators=[InputRequired('Password is required'),
                             Length(min=5,max=10, message='Type 5 to 10 characters.'),
                             AnyOf(values=['password','secret'])])

# Route do strony glownej
@app.route('/')
def home():
    return render_template('home.html')

# Route do przykladowego formularza
@app.route('/form', methods=['GET','POST'])
def form():
    form = LoginForm()

    if form.validate_on_submit(): #jesli formularz zostal wyslany, to zwracamy info
        return '<h1>The username is {}. The password is {}.</h1>'.format(form.username.data, form.password.data)
    return render_template('form.html', form=form)

# Tymczasowy run dla debugu z przegladarki - ustawic pozniej np. na localhost:80
if __name__ == '__main__':
    app.run(debug=True)
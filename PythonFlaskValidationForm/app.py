from flask import Flask, render_template
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, TextAreaField, RadioField, SelectField, EmailField
from wtforms.validators import InputRequired, Length, AnyOf

# podanie sciezki do template'ow HTML
app = Flask(__name__, template_folder='templates')

# secret key
app.config['SECRET_KEY'] = 'Thisisasecret!'
# klucze ReCaptcha
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lc1U9UkAAAAANTZA0OfJBiQZUzSUrVgeS3ieBzd'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lc1U9UkAAAAAIE6Du4fHcqgIVQbkI_Eckt--NWB'
app.config['TESTING'] = True # jezeli wartosc true, to Flask wie ze testujemy aplikacje (nie jest "na produkcji")
                              # np. mozna ominac wtedy Captcha

class LoginForm(FlaskForm):
    email = EmailField('email',
                             validators=[InputRequired('Email is required')])

    username = StringField('username',
                             validators=[InputRequired('Username is required'),
                             Length(min=5,max=10, message='Type 5 to 10 characters.')])

    password = PasswordField('password',
                             validators=[InputRequired('Password is required'),
                             Length(min=5,max=10, message='Type 5 to 10 characters.'),
                             AnyOf(values=['password','secret'])])

    textarea = TextAreaField('TextArea')

    radios = RadioField('Radios', default='option1', choices=[('option1', 'Option one is this.'), ('option2', 'Option two is this.')])

    selects = SelectField('Select', choices=[('1','1'), ('2','2'), ('3','3')])

    recaptcha = RecaptchaField()

# Route do przykladowego formularza
@app.route('/', methods=['GET','POST'])
def form():
    form = LoginForm()

    if form.validate_on_submit(): #jesli formularz zostal wyslany, to zwracamy info
        return render_template('results.html',
                               email=form.email.data,
                               username=form.username.data,
                               password=form.password.data,
                               textarea=form.textarea.data,
                               radios=form.radios.data,
                               selects=form.selects.data)

    return render_template('form.html', form=form)

@app.route('/results')
def results():
    
    return render_template('results.html')

# Tymczasowy run dla debugu z przegladarki - ustawic pozniej np. na localhost:80
if __name__ == '__main__':
    app.run(debug=True)
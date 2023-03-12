from flask import Flask, render_template
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileRequired, FileAllowed 
from wtforms import StringField, PasswordField, TextAreaField, RadioField, SelectField, EmailField, FileField
from wtforms.validators import InputRequired, Length, AnyOf
from flask_uploads import configure_uploads, IMAGES, UploadSet

# podanie sciezki do template'ow HTML
app = Flask(__name__, template_folder='templates')

# secret key
app.config['SECRET_KEY'] = 'Thisisasecret!'
# klucze ReCaptcha  
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lc1U9UkAAAAANTZA0OfJBiQZUzSUrVgeS3ieBzd' # https://www.google.com/recaptcha/admin/create
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lc1U9UkAAAAAIE6Du4fHcqgIVQbkI_Eckt--NWB' # https://www.google.com/recaptcha/admin/create
app.config['TESTING'] = True # jezeli wartosc true, to Flask wie ze testujemy aplikacje (nie jest "na produkcji") np. mozna ominac wtedy Captcha
app.config['UPLOADED_IMAGES_DEST'] = 'static/uploads/images'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

class LoginForm(FlaskForm):
    email = EmailField('E-mail:',
                             validators=[InputRequired('Email is required')])

    username = StringField('Username:',
                             validators=[InputRequired('Username is required'),
                                         Length(min=5,max=10,
                                         message='Type 5 to 10 characters.')])

    password = PasswordField('Password:',
                             validators=[InputRequired('Password is required')])

    """
    avatar = FileField('Avatar:', validators=[FileRequired(),
                                               FileAllowed(ALLOWED_EXTENSIONS, message='Images only! (PNG,JPEG,GIF)')])
    """
    avatar = FileField('Avatar:', validators=[FileRequired(), FileAllowed(ALLOWED_EXTENSIONS, message='Images only! (PNG,JPEG,GIF)')])

    textarea = TextAreaField('Few words about me:') 

    radios = RadioField('Gender:', choices=[('Male', 'Male'), # ('optionName','visible text of option in form')
                                            ('Female', 'Female'),
                                            ('Secret', 'Secret')],
                                   default='Secret')

    selects = SelectField('Favourite programming language:', choices=[('C++','C++'),
                                                                      ('C#','C#'),
                                                                      ('Java','Java'),
                                                                      ('JavaScript','JavaScript'),
                                                                      ('Python','Python')],
                                                             default='Python')

    mathQuestion = StringField('2 plus 4 equals:', validators=[AnyOf(values=['six','6'], message='Please type one of: six, 6')])

    recaptcha = RecaptchaField()

# Route do przykladowego formularza
@app.route('/', methods=['GET','POST'])
def form():
    form = LoginForm()

    filename = None
    file_url = None

    if form.validate_on_submit(): #jesli formularz zostal wyslany, to zwracamy info
        filename = images.save(form.avatar.data)
        file_url = images.url(filename)
        return render_template('results.html',
                            email=form.email.data,
                            username=form.username.data,
                            password=form.password.data,
                            avatar=form.avatar.data,
                            textarea=form.textarea.data,
                            radios=form.radios.data,
                            selects=form.selects.data)

    return render_template('form.html', form=form, file_url=file_url)

@app.route('/results')
def results():
    
    return render_template('results.html')

# Tymczasowy run dla debugu z przegladarki - ustawic pozniej np. na localhost:80
if __name__ == '__main__':
    app.run(debug=True)
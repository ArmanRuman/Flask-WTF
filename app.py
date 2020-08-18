from flask import Flask,render_template
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField,PasswordField,IntegerField,BooleanField,Form,FormField,ValidationError
from wtforms.validators import InputRequired,Length,AnyOf,Email
from wtforms.fields.html5 import DateField
app=Flask(__name__)
app.config['SECRET_KEY']='secretkey'
app.config['WTF_CSRF_ENABLED']=True
app.config['WTF_CSRF_TIME_LIMIT']=1800
app.config['RECAPTCHA_PUBLIC_KEY']='6LdPMrcZAAAAAHiS-wB0qv1DZnJyA_oHFA7VIqO1'
app.config['RECAPTCHA_PRIVATE_KEY']='6LdPMrcZAAAAAJMQZmJL5gaY5G87mrxbE_rsg3lT'

class DynamicForm(FlaskForm):
    entrydate=DateField("Date:")
    


class TelephoneForm(Form):
    country_code=IntegerField('Country Code:')
    area_code=IntegerField('Area Code:')
    number=StringField('Phone Number:')

class LoginForm(FlaskForm):
    username=StringField('Username',validators=[InputRequired(),Length(min=3,max=8,message='Your username does not validate!')])
    email=StringField('Email',validators=[Email()])
    password=PasswordField('Password',validators=[InputRequired()])
    age=IntegerField('Age:')
    yesno=BooleanField('Yes/No')
    home_phone=FormField(TelephoneForm)
    recaptcha=RecaptchaField('recaptcha')

    def validate_username(form,field):
        if field.data =='Arman':
            raise ValidationError('You have not correct name!')

@app.route('/',methods=['GET','POST'])
def home():
    form=LoginForm()
    if form.validate_on_submit():
        return f'<h3> Country Code:{form.home_phone.country_code.data},Area Code:{form.home_phone.area_code.data},Number:{form.home_phone.number.data} </h3>'
        #return f'<h1> Username:{form.username.data},Email:{form.email.data},Password:{form.password.data},Age:{form.age.data},Yes/No:{form.yesno.data}</h1>'
    return render_template('index.html',form=form)

@app.route('/dynamic',methods=['GET','POST'])
def dynamic():
    DynamicForm.name=StringField('Name')
    names=['First_Name','Last_Name','Nickname']
    for name in names:
        setattr(DynamicForm,name,StringField(name))
 
    form=DynamicForm()
    if form.validate_on_submit():
        return f'Date:{form.entrydate.data},Name:{form.name.data},Nickname:{form.Nickname.data}'

    return render_template('dynamic.html',form=form,names=names)

if __name__=='__main__':
    app.run(debug=True)


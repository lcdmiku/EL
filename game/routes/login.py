from flask import render_template, request, redirect, url_for,Blueprint,session
from wtforms import StringField,PasswordField,SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,EqualTo
from game import db
from game.models.user import User


login_bp = Blueprint('login', __name__)
message = ''
@login_bp.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        choice = request.form['choice']
        if choice == 'login':
            return redirect(url_for('login.login'))
        elif choice == 'register':
            return redirect(url_for('login.register'))

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired('cannot be empty')])
    password = PasswordField('Password',validators=[DataRequired('cannot be empty')])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('cannot be empty')])
    password = PasswordField('Password', validators=[DataRequired('cannot be empty')])
    password2 = PasswordField('Password 2', validators=[DataRequired('cannot be empty'), EqualTo('password')] )
    submit = SubmitField('Register')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html',form = form)
    elif request.method == 'POST':
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            return render_template('login.html',form=form,message='username or password is incorrect')
        else:
            #if success,set session
            session['user_id'] = user.id
            return redirect(url_for('play.play'))


@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html',form = form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            if User.query.filter_by(username=username).first():#if username have existed,it is incorrect
                return render_template('register.html',form=form,message='username have been registered')
            password = form.password.data
            user = User(username=username,password=password)
            user.save()
            # if success,set session
            session['user_id'] = user.id
            return redirect(url_for('play.play'))
        else:
            return render_template('register.html',form=form,message='username or password is invalid')

@login_bp.route('/logout')
def logout():
    session.pop('user_id',None)
    return redirect(url_for('login.login'))
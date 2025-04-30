from flask import render_template, request, redirect, url_for, Blueprint, session, jsonify
from pyexpat.errors import messages
from wtforms import StringField,PasswordField,SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,EqualTo

from game.models.user import User


login_bp = Blueprint('login', __name__)


class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired('cannot be empty')])
    password = PasswordField('Password',validators=[DataRequired('cannot be empty')])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('cannot be empty')])
    password = PasswordField('Password', validators=[DataRequired('cannot be empty')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired('cannot be empty'), EqualTo('password')] )
    submit = SubmitField('Register')

@login_bp.route('/',methods=['GET','POST'])
def index():
    login_form = LoginForm()
    register_form = RegisterForm()
    if request.method == 'GET':
        return render_template('index.html',login_form=login_form,register_form=register_form)
    elif request.method == 'POST':
        if  login_form.submit.data:
            return redirect(url_for('login.login'))
        elif register_form.submit.data :
            return redirect(url_for('login.register'))

@login_bp.route('/login', methods=['POST'])
def login():
    login_form = LoginForm()

    if request.method == 'POST':
        username = login_form.username.data
        password = login_form.password.data
        print(username,password)
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            return jsonify({"action":"login","message": 'username or password is incorrect'})
        else:
            #if success,set session
            session['user_id'] = user.id
            return jsonify({'redirect': url_for('play.play')})



@login_bp.route('/register', methods=['POST'])
def register():
    register_form = RegisterForm()

    if request.method == 'POST':
        if register_form.validate_on_submit():
            username = register_form.username.data
            if User.query.filter_by(username=username).first():#if username have existed,it is incorrect
                return render_template('index.html',register_form=register_form,message='username have been registered')
            password = register_form.password.data
            user = User(username=username,password=password)
            user.save()
            # if success,set session
            session['user_id'] = user.id
            return jsonify({"redirect": url_for('play.play')})
        else:
            return jsonify({"action":"register","message" : 'username or password is invalid'})

@login_bp.route('/logout')
def logout():
    session.pop('user_id',None)
    return redirect(url_for('login.index'))
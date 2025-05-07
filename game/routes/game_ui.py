from flask import render_template, Blueprint, session, redirect, url_for, request
from wtforms import StringField, PasswordField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo
from game import db
from game.models.user import User
from .login import LoginForm

ui_bp = Blueprint('ui', __name__)
#登陆成功后进入的页面

class UIForm(FlaskForm):
    choices = SelectField('Choices', choices=[('play', 'Play'), ('read', 'Read'), ('write', 'Write')])
    submit = SubmitField('Submit')


@ui_bp.route('/ui', methods=['GET', 'POST'])
def game_ui():
    current_user = User.current_user(session)
    if current_user:
        form = UIForm()
        if request.method == 'GET':
            return render_template('index.html', current_user=current_user, form=form)
        elif request.method == 'POST':
            if form.validate_on_submit():
                choice = form.choices.data
                # 这里假设 play 蓝图存在，你需要根据实际情况修改
                return redirect(url_for(f'play.{choice}'))
    else:
        return redirect(url_for('login.login'))

#游戏场景信息，采用字典存储
Map = [{'id':1,
    "address": "Address 1",

        "background_image": "/static/images/address1_bg.jpg",
        "music_file": "/static/music/address1_music.mp3"},
       {   'id':2,
           "address": "Address 2",

        "background_image": "/static/images/address2_bg.png",
        "music_file": "/static/music/address2_music.mp3", }
]
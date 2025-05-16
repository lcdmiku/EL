from flask import render_template, Blueprint, session, redirect, url_for, request
from wtforms import StringField, PasswordField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo

from game.models.user import User
from game.models.NPC import NPC,create_npc
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

#NPC
dialogs_1 = [
    {
        "player_dialog":"是的",
        "npc_dialog": "你还喜欢这里吗",
        "npc_name": "Andy",
        "npc_portrait": "/static/images/npc1.png",
    },
{
        "player_dialog":"是",
        "npc_dialog": "你hen喜欢这里吗",
        "npc_name": "Andy",
        "npc_portrait": "/static/images/npc1.png",
    }

]

dialogs_2 = [
    {
        "player_dialog": "thank",
        "npc_dialog": "welcome!",
        "npc_name": "Any",
        "npc_portrait": "/static/images/npc2.png",
     },
{
        "player_dialog": "thank",
        "npc_dialog": "we come!",
        "npc_name": "Any",
        "npc_portrait": "/static/images/npc2.png",
     }

]

NPC_1 = create_npc('Andy',"/static/images/npc1.png", dialogs_1)
NPC_2 = create_npc('Any',"/static/images/npc2.png",dialogs_2)
npc_data_1 = NPC_1.to_dict()
npc_data_2 = NPC_2.to_dict()



#游戏场景信息，采用字典存储
Map = [
    {
        'id': 1,
        "address": "Address 1",
        "background_image": "/static/images/address1_bg.jpg",
        "music_file": "/static/music/address1_music.mp3",
        "npc":npc_data_1,
    },
    {
        'id': 2,
        "address": "Address 2",
        "background_image": "/static/images/address2_bg.png",
        "music_file": "/static/music/address2_music.mp3",
        "npc":npc_data_2,
    }
]
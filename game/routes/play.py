from contextlib import nullcontext

from flask import render_template, Blueprint, request, redirect, url_for, session, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField,TextAreaField
from wtforms.fields.simple import HiddenField
from wtforms.validators import DataRequired
#sql
from sqlalchemy import and_
from..models.user import *
from ..models.NPC import NPC

from.game_ui import Map


play_bp = Blueprint('play', __name__)

#全局函数
map_info = Map[0]#只会在视图函数play中改变
# 默认地图为 Map[0]

def get_current_user_and_map_info():
    """防止在play函数之外的地方改变map_infor 和 current_user"""
    try:
        current_user = User.current_user(session)
    except:
        current_user = None
        redirect(url_for('login.login'))
    return current_user, map_info
# 辅助函数，将 current_user 作为参数传入
def get_letters(current_user, letter_type):
    if letter_type == 'written_letters':
        return current_user.written_letters.all()
    elif letter_type =='received_letters':
        return current_user.received_letters.all()
    elif letter_type == 'viewed_letters':
        return current_user.viewed_letters.all()
    elif letter_type == 'written_news':
        return current_user.written_news.all()
    else:
        return None


def help_write(current_user, form,map_info=map_info,reply_to_id=None):
    if current_user:
        if form.validate_on_submit():
            content = form.content.data
            title = content[:5]+'...'#将title改为content的前五个字符
            signature = form.signature.data
            content = content + '\n' +f"Yours {signature}"
            address_id = map_info['id']
            show_writer = form.show_writer.data

            writer_id = current_user.id
            letter = Letter(title=title, content=content, address_id=address_id,addressee_id=reply_to_id,
                            Is_show_writer=show_writer, writer_id=writer_id)#去掉addressee

            letter.save()
            return 'Letter saved successfully'
        return 'Invalid form'
    return 'Please log in to write a letter'


def help_read(current_user, form):
    letter_type = form.letter_type.data
    letters = get_letters(current_user, letter_type)
    return letters


class PlayChoice(FlaskForm):
    operations = HiddenField('operations')
    read_btn = SubmitField('Read')
    write_btn = SubmitField('Write')
    collect_btn = SubmitField('Collect')
    play = SelectField('Location', choices=[('0', 'Address 1'), ('1', 'Address 2'), ('2', 'Address 3')],  default=0)
    submit = SubmitField('Submit')

    def get_operations(self):
        """得到前端user的操作"""
        if self.read_btn.data:
            return'read'
        if self.write_btn.data:
            return 'write'
        if self.collect_btn.data:
            return 'collect'
        if self.play.data:
            return'map'


class Read(FlaskForm):
    letter_type = SelectField('Type', choices=[('written_letters', 'Written Letter'), ('received_letters', 'Received Letter'), ('viewed_letters', 'Viewed Letter'), ('written_news', 'Written News')])
    submit = SubmitField('Submit')


class Write(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    signature = StringField('Signature', validators=[])#去除标题,改为写信者的署名
    addressee = StringField('Addressee')  # can be none
    # address needn't be provided by user
    # address = SelectField('Address', choices=[(0, 'Address 1'), (1, 'Address 2')], coerce=int, default=0)
    show_writer = BooleanField('Show Writer')  # 默认为false
    submit = SubmitField('Submit')


@play_bp.route('/play', methods=['GET', 'POST'])
def play():
    global map_info
    #map_info只能在play中改变,其他函数得到的均是map_info的copy
    form = PlayChoice()
    read_form = Read()
    write_form = Write()
    try:
        current_user = User.current_user(session)
    except:
        return redirect(url_for('login.login'))

    if not current_user:
        return redirect(url_for('login.login'))

    if request.method == 'GET':
        return render_template('play.html', form=form, map_info=map_info, read_form=read_form, write_form=write_form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            # 监听用户所执行的操作
            operation = form.get_operations()
            if operation =='read':
                return redirect(url_for('play.read'))
            elif operation == 'write':
                return redirect(url_for('play.write'))
            elif operation == 'collect':
                return redirect(url_for('play.collect'))
            elif operation =='map':
                # 换场景
                map_choice = int(form.play.data)
                if 0 <= map_choice < len(Map):
                    map_info = Map[int(map_choice)]
                print(map_info,map_choice)
            return jsonify({'action':'play',"map_info":map_info})
        return render_template('play.html', form=form, message='Invalid form', map_info=map_info, read_form=read_form, write_form=write_form)


@play_bp.route('/read', methods=['POST'])
def read():
    current_user, map_info = get_current_user_and_map_info()
    form = Read()
    if form.validate_on_submit():
        letters = help_read(current_user, form)
        current_user_info = current_user.to_dict()
        letter_list = [{"title": letter.title, "content": letter.content,"writer_id":letter.writer_id} for letter in letters] if letters else []
        print(letter_list)
        return jsonify({"action": "read", "letters": letter_list,"user_info":current_user_info})
    return jsonify({"action": "read", "error": "Invalid form"})


@play_bp.route('/write', methods=['POST'])
def write():
    current_user, map_info = get_current_user_and_map_info()
    form = Write()
    form_data = request.form
    reply_to_id = form_data.get('reply_to_id')
    print(form_data,form)
    if form.validate_on_submit():
        message = help_write(current_user, form, map_info=map_info,reply_to_id=reply_to_id)
        return jsonify({"action": "write", "message": message})


@play_bp.route('/collect', methods=['POST'])
def collect():
    current_user, map_info = get_current_user_and_map_info()
    address_id = map_info['id']
    print(address_id, map_info)
    letter = Letter.query.filter(
        and_(
            Letter.address_id == address_id,
            Letter.Is_viewed == False,
            Letter.addressee_id == ''

        )
    ).first()#TODO Letter.writer_id != current_user.id

    if letter is None:#竟然是空字符，fuck
        print('tell me why')
    else:
        print('value',type(letter.addressee_id),letter.addressee_id)
    if letter:
        letter.Is_viewed = True
        letter.viewer_id = current_user.id
        letter.save()
        letter_dic = letter.to_dict()
        return jsonify({"action": "collect", "message": "Letter collected successfully",'letter': letter_dic})
    return jsonify({"action": "collect", "error": "No letter to collect"})


@play_bp.route('/myself_info', methods=['POST'])
def myself_info():
    current_user, map_info = get_current_user_and_map_info()
    user_info = current_user.to_dict()
    return jsonify({"action": "myself_info", "user_info": user_info})

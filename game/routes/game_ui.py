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

NPC_1 = create_npc('陆知远',"/static/images/npc1.png",
                   [
                       {"dialog": "（手忙脚乱按掉语音，整张脸烧起来）对、对不起！吵到你了（偷瞄对面的张紫悠，却发现她正盯着自己笑）",
                        "image_A": "/static/images/npc1_A.png",
                        "image_B": "/static/images/npc1_B.png"},
                       {"dialog": "（把草稿纸递过来，纸上用铅笔写着一行字）：没事，你刚刚外放的是周杰伦的《告白气球》吧？其实我也经常忘关外放。",
                        "image_A": "/static/images/npc1_A.png",
                        "image_B": "/static/images/npc1_B.png"},
                       {"dialog": "（在纸上回）原来你也喜欢周杰伦！",
                        "image_A": "/static/images/npc1_A.png",
                        "image_B": "/static/images/npc1_B.png"},
                       {"dialog": "（有点小激动，在纸上回）上次去周杰伦的音乐节，我好想看见你了。",
                        "image_A": "/static/images/npc1_A.png",
                        "image_B": "/static/images/npc1_B.png"},
                       {"dialog": "（手指攥紧笔，心跳得快要冲出胸腔，写下）我那天好像也看见你了。",
                        "image_A": "/static/images/npc1_A.png",
                        "image_B": "/static/images/npc1_B.png"},
                       {"dialog": "（回想起那天两人并没有离得很近，在如此多人的情况下竟然能找到自己，意识到对方好像也在关注自己，决定勇敢一次，在纸上写下）其实，我去音乐节不只是因为一个人...",
                        "image_A": "/static/images/npc1_A.png",
                        "image_B": "/static/images/npc1_B.png"},
                       {"dialog": "（明白了张紫悠的意思，决定表明心意，写下）我也是呢...不瞒你说，我在第一次音乐社的活动上，就喜欢上你了...",
                        "image_A": "/static/images/npc1_A.png",
                        "image_B": "/static/images/npc1_B.png"},
                       {"dialog": "（看到草稿纸愣了一愣，随即转为欣喜，把一只耳机递给陆知远）",
                        "image_A": "/static/images/npc1_A.png",
                        "image_B": "/static/images/npc1_B.png"},
                       {"dialog": "（戴上耳机，听见耳机里面播放的正是《告白气球》）",
                        "image_A": "/static/images/npc1_A.png",
                        "image_B": "/static/images/npc1_B.png"},
                   ]
                   )
NPC_2 = create_npc('叶昱凌',"/static/images/npc2.png",
                   [
                       {"dialog": "（凑过来）又卡在动态规划？上周你教我做数据库的时候，可不是这副蔫头耷脑的样子。",
                        "image_A": "/static/images/npc2_A.png",
                        "image_B": "/static/images/npc2_B.png"},
                       {"dialog": "（吸了吸鼻子）我就是觉得自己太笨了，算法作业改了七版还是不对，竞赛也没进复赛，以后怎么找工作啊...",
                        "image_A": "/static/images/npc2_A.png",
                        "image_B": "/static/images/npc2_B.png"},
                       {"dialog": "（抽出草稿纸，随手画了个歪歪扭扭的流程图）你看，计算机的世界多公平，再复杂的问题都能拆解成小模块。现在卡住的这点困难，不过是整个系统里面的一个子函数而已。",
                        "image_A": "/static/images/npc2_A.png",
                        "image_B": "/static/images/npc2_B.png"},
                       {"dialog": "（盯着流程图，喉咙发紧）可别人都好厉害，我总担心...",
                        "image_A": "/static/images/npc2_A.png",
                        "image_B": "/static/images/npc2_B.png"},
                       {"dialog": "担心什么？担心明天太阳不会照常升起？真正的大佬，都是从把报错当早安问候开始的",
                        "image_A": "/static/images/npc2_A.png",
                        "image_B": "/static/images/npc2_B.png"},
                       {"dialog": "（噗嗤笑出声，拿笔戳了戳他画的流程图）那按你的算法，这个子函数该怎么调用？",
                        "image_A": "/static/images/npc2_A.png",
                        "image_B": "/static/images/npc2_B.png"},
                       {"dialog": "（把椅子挪近，屏幕亮光映着两张年轻的脸）首先，调用“深呼吸”函数清空缓存，再实例化一个“睡足七小时类”...记住，编译器不会欺骗每个认真调试的人。",
                        "image_A": "/static/images/npc2_A.png",
                        "image_B": "/static/images/npc2_B.png"},
                   ]
                   )
NPC_3 = create_npc('曹景霄', "/static/images/npc3.png",
                   [
                       {"dialog": "（从厨房出来，坐在曹景霄对面）孩子，爸跟你说个事儿。爸思来想去，你本科毕业就去考公务员吧，这工作稳定，待遇也好。",
                        "image_A": "/static/images/npc3_A.png",
                        "image_B": "/static/images/npc3_B.png"},
                       {"dialog": "（放下手里的考研资料，抬起头）爸，我不想考公，我想考研，以后搞科研。",
                        "image_A": "/static/images/npc3_A.png",
                        "image_B": "/static/images/npc3_B.png"},
                       {"dialog": "（微微皱眉，神情有些严肃）科研哪有那么容易，多辛苦啊，还不一定有成果。公务员多省心，旱涝保收的。",
                        "image_A": "/static/images/npc3_A.png",
                        "image_B": "/static/images/npc3_B.png"},
                       {"dialog": "（眼神坚定地看着父亲）爸，我知道科研难，但我真的喜欢。我想在自己热爱的领域深入探索，这是我的梦想。考公不是我想要的生活，每天按部就班，我怕会失去冲劲。",
                        "image_A": "/static/images/npc3_A.png",
                        "image_B": "/static/images/npc3_B.png"},
                       {"dialog": "（沉默片刻，叹了口气）你这孩子，梦想能当饭吃吗？你要是搞科研，以后生活压力大，爸是心疼你，不想你吃苦。",
                        "image_A": "/static/images/npc3_A.png",
                        "image_B": "/static/images/npc3_B.png"},
                       {"dialog": "（有些着急）爸，我不怕吃苦。我知道您是为我好，担心我以后生活不好。但如果我放弃梦想去考公，我可能一辈子都不会开心。我已经长大了，想为自己的选择负责。",
                        "image_A": "/static/images/npc3_A.png",
                        "image_B": "/static/images/npc3_B.png"},
                       {"dialog": "（缓缓点头，脸上的神情缓和了许多）唉，爸也知道不该拦着你追求梦想。爸就是担心你以后过得不好。既然你这么坚定，那爸支持你考研搞科研。",
                        "image_A": "/static/images/npc3_A.png",
                        "image_B": "/static/images/npc3_B.png"},
                       {"dialog": "（露出了期待的神情）爸，谢谢您理解我！我知道您是为我考虑，我会努力的，不会让您失望。我会兼顾好科研和生活，照顾好自己的。",
                        "image_A": "/static/images/npc3_A.png",
                        "image_B": "/static/images/npc3_B.png"},
                       {"dialog": "（拍了拍曹景霄的肩膀）行，那你就好好准备考研。要是有啥困难，跟爸说。",
                        "image_A": "/static/images/npc3_A.png",
                        "image_B": "/static/images/npc3_B.png"},
                       {"dialog": "（和父亲相视一笑）好嘞，爸！我会加油的！",
                        "image_A": "/static/images/npc3_A.png",
                        "image_B": "/static/images/npc3_B.png"},
                   ]
                   )
npc_data_1 = NPC_1.to_dict()
npc_data_2 = NPC_2.to_dict()
npc_data_3 = NPC_3.to_dict()
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
        "npc":npc_data_2
    },
    {
        'id': 3,
        "address": "Address 3",
        "background_image": "/static/images/address3_bg.jpg",
        "music_file": "/static/music/address2_music.mp3",
        "npc":npc_data_3
    }
]
from email.policy import default

from sqlalchemy.orm import backref, relationship

from game import db
#the class of user and text(letters and news)
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)#为每个用户分配id,类似qq账号
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(32))
    # role_id = db.Column(db.Integer, db.ForeignKey(Role.id))
    #user's letters
    written_letters = db.relationship('Letter', backref='writer', lazy='dynamic', foreign_keys='Letter.writer_id')#user 写的信
    received_letters = db.relationship('Letter', backref='receiver', lazy='dynamic', foreign_keys='Letter.addressee_id')#收的信
    viewed_letters = db.relationship('Letter', backref='viewer', lazy='dynamic', foreign_keys='Letter.viewer_id')
    #if the letter have addressee,viewer is addressee
    #by the way,one letter can be only read by only one person
    #news's about
    # written_news = db.relationship('News', backref='writer', lazy='dynamic', foreign_keys='News.writer_id')

    # # 新增：故事进度字段
    # story_progress = db.Column(db.Integer, default=0)  # 0=未开始, 1=进行中, 2=已完成
    #
    # # 新增：故事成就字段
    # story_achievements = db.Column(db.String(256), default='')  # 存储成就ID，逗号分隔

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_password(self, password):
        if self.password == password:
            return True
        else:
            return False

    def save(self):#save the data into database
        db.session.add(self)
        db.session.commit()

    def to_dict(self, fields=None):
        """
        将 User 对象转换为字典形式。
        :param fields: 可选参数，指定要包含在返回字典中的属性名称列表。
                       如果为 None，则返回默认的属性集合（不包含密码）。
        :return: 包含用户信息的字典。
        """
        default_fields = ['id', 'username', 'written_letters', 'received_letters', 'viewed_letters']
        if fields:
            data = {field: getattr(self, field) for field in fields if hasattr(self, field)}
        else:
            data = {
                'id': self.id,
                'username': self.username,
                'written_letters': [letter.title for letter in self.written_letters],
                'received_letters': [letter.title for letter in self.received_letters],
                'viewed_letters': [letter.title for letter in self.viewed_letters],
                # 'written_news': [news.title for news in self.written_news]
            }
        return data

    @staticmethod
    def current_user(session):
        user_id = session.get('user_id')
        if user_id:
            return User.query.get(int(user_id))
        else:
            return None


class Text(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # content
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.String(128), nullable=False)
    #  other detail
    Is_show_writer = db.Column(db.Boolean, default=False)  # whether writer's id or name is shown

    def save(self):
        db.session.add(self)
        db.session.commit()

class Letter(Text):
    __tablename__='letter'
    #address and other detail
    address_id = db.Column(db.Integer,nullable=False)#where writer put letters
    #writer,addressee,and viewer
    writer_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    addressee_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=True)#收信件的人可有可无
    viewer_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=True)
    #确定是否已阅
    Is_viewed = db.Column(db.Boolean,default=False)
    #reply letter
    # reply_id = db.Column(db.Integer,db.ForeignKey('letter.id'),nullable=True)
    # replied_letter=db.relationship('Letter', backref='reply', lazy='dynamic', foreign_keys='Letter.reply_id')

    def to_dict(self):
        """将letter对象可json化的数据保存到字典中以便前端使用"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'Is_show_writer': self.Is_show_writer,
            'address_id': self.address_id,
            'writer_id': self.writer_id,
            'addressee_id': self.addressee_id,
            'viewer_id': self.viewer_id,
            'Is_viewed': self.Is_viewed
        }



# news_reader = db.Table('news_reader',
#                        db.Column('id', db.Integer, primary_key=True, autoincrement=True),
#                        db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
#                        db.Column('news_id',db.Integer,db.ForeignKey('news.id')),
#                        )
#
# class News(Text):
#     __tablename__='news'
#     views_count = db.Column(db.Integer,default=0)
#     writer_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
#     #build to viewer
#     to_viewer = db.relationship('User',
#                                 secondary= news_reader ,
#                                 backref = db.backref('viewed_news',lazy='dynamic'),
#                                 lazy='dynamic',
#                                 )
#     #the id of the news board
#     board_id = db.Column(db.Integer,nullable=False)
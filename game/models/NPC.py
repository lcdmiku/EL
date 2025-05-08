from game import db

#NPC的类，后端继续写

class NPC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    #
    x_position = db.Column(db.Integer, default=0)  # NPC 的 x 坐标
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "x_position": self.x_position
        }
    #
from werkzeug.security import generate_password_hash, check_password_hash
from .base_model import db
# from .msg_model import Message


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)
        # self.messages = Message.query.filter_by(sender_id=int(self.id))

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            # 'messages': self.messages
        } 


class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        unique=True
    )

    system_prompt = db.Column(db.Text)
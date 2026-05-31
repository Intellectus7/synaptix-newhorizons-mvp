from .base_model import db

class BotB(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        unique=False
    )

    system_prompt = db.Column(db.Text)
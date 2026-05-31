from flask_sqlalchemy import SQLAlchemy
from .base_model import db
from .group_model import Group
from datetime import datetime


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # sender 
    sender_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )

    sender = db.relationship(
        'User',
        foreign_keys=[sender_id],
        backref='sent_messages'
    )

    # receiver (direct chats)
    receiver_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=True
    )

    receiver = db.relationship(
        'User',
        foreign_keys=[receiver_id],
        backref='received_messages'
    )

    # group chats
    group_id = db.Column(
        db.Integer,
        db.ForeignKey('group.id'),
        nullable=True
    )

    group = db.relationship(
        'Group',
        backref='messages'
    )

    content = db.Column(db.Text)

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    
    def to_dict(self):
        print("Printing to dictionary")
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'reciever_id': self.receiver_id,
            'group_id': self.group_id,
            'content': self.content,
            'timestamp': self.timestamp      
        }
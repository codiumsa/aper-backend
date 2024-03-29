from flask_login import UserMixin
from flask import current_app
from sqlalchemy import Column, Integer, String, Date, or_
from sqlalchemy.sql.expression import func
from .db import Base, db_session
from datetime import date


class User(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer,
                primary_key=True)  # primary keys are required by SQLAlchemy
    email = Column(String(100), unique=True)
    name = Column(String(100))
    order = Column(Integer, nullable=False)
    absent_on = Column(Date)

    def __init__(self, name, email):
        self.email = email
        self.name = name
        max_order = db_session.query(func.max(User.order)).scalar()
        self.order = max_order + 1 if max_order else 1
        self.absent_on = None

    def serialize(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'order': self.order,
            'absent_on': self.absent_on
        }

    @classmethod
    def allowed_users(cls):
        return cls.query.filter(
            or_(cls.absent_on != str(date.today()),
                cls.absent_on == None)).order_by(cls.order).limit(
                    current_app.config['QUEUE_SIZE']).all()

    def __repr__(self):
        return '<User {}[{}]>'.format(self.name, self.email)

    def __eq__(self, value):
        return self.id == value.id and self.name == value.name and self.order == value.order and self.absent_on == value.absent_on

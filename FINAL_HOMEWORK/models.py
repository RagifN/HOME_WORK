from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mynewsdatabase.db'
db = SQLAlchemy(app)


class UserDate(BaseModel):
    id: int
    name: str
    surname: str


class UserIn(BaseModel):
    name: str
    surname: str


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'{self.firstname} {self.lastname}'


class TheGoods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goods_name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    price = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'{self.goods_name} {self.description} {self.price}'


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    goods_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    date = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    user = db.relationship('Users', backref=db.backref('orders', lazy=True))
    goods = db.relationship('Goods', backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return f'{self.date} {self.status}'

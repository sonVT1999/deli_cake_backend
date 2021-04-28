# coding: utf-8
from app.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.int, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.int, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.int)
    category = db.Column(db.String(100), nullable=False)
    subcategory = db.Column(db.String(100), nullable=False)


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.int, primary_key=True)
    name = db.Column(db.String(100))


class Subcategory(db.Model):
    __tablename__ = 'subcategories'

    id = db.Column(db.int, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(100), nullable=False)


class Order(db.Model):
    __tablename__ = 'orders '

    id = db.Column(db.int, primary_key=True)
    total = db.Column(db.Float())
    status = db.Column(db.String(20))
    phone_number = db.Column(db.String(12))
    address = db.Column(db.String(100))

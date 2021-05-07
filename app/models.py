# coding: utf-8
from sqlalchemy import ForeignKey

from app.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))
    phone_number = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean(), nullable=False)


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))
    direction = db.Column(db.String(255), nullable=False)
    ingredient = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255))
    publish_at = db.Column(db.Integer, nullable=False)

    def json(self):
        return {'id': self.id, 'name': self.name, 'direction': self.direction, 'ingredient': self.ingredient,
                'image': self.image, 'publish_at': self.publish_at}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))

    def json(self):
        return {'id': self.id, 'name': self.name}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


class Subcategory(db.Model):
    __tablename__ = 'subcategories'

    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))
    category_id = db.Column(ForeignKey(Category.id), nullable=False)

    def json(self):
        return {'id': self.id, 'name': self.name, 'category_id': self.category_id}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id_category(cls, _id):
        return cls.query.filter_by(category_id=_id).all()

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()



class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float())
    product_detail = db.Column(db.String(100))
    size = db.Column(db.String(50))
    subcategory_id = db.Column(ForeignKey(Subcategory.id), nullable=False)
    recipe_id = db.Column(ForeignKey(Recipe.id))

    def json(self):
        return {'id': self.id, 'name': self.name, 'price': self.price, 'product_detail': self.product_detail,
                'size': self.size}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id_subcategory(cls, _id):
        return cls.query.filter_by(subcategory_id=_id).all()

    @classmethod
    def get_by_id_recipe(cls, _id):
        return cls.query.filter_by(recipe_id=_id).first()

class Status(db.Model):
    __tablename__ = 'status'

    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.String(100), primary_key=True)
    total = db.Column(db.Float, nullable=False)
    created_date = db.Column(db.Integer, nullable=False)
    status_id = db.Column(ForeignKey(Status.id), nullable=False)
    user_id = db.Column(ForeignKey(User.id), nullable=False)


class Order_detail(db.Model):
    __tablename__ = 'orders_details'

    id = db.Column(db.String(100), primary_key=True)
    order_id = db.Column(ForeignKey(Order.id), nullable=False)
    item_id = db.Column(ForeignKey(Item.id), nullable=False)
    amount = db.Column(db.Integer, nullable=False)


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))
    item_id = db.Column(ForeignKey(Item.id), nullable=False)

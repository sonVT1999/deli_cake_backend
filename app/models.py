# coding: utf-8
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

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

    def json(self):
        return {'id': self.id, 'username': self.username, 'password': self.password, 'address': self.address,
                'phone_number': self.phone_number, 'email': self.email, 'is_admin': self.is_admin}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_all_detail(cls, _id):
        rs = (cls.query.join(Order, cls.id == Order.user_id)
              .join(Order_detail, Order.id == Order_detail.order_id)
              .join(Item, Item.id == Order_detail.item_id)
              .add_columns(Item.id, Item.name, Order_detail.amount, Item.price, Order.total)
              .filter(Order.id == _id)).all()
        return rs

    @classmethod
    def get_all_user(cls):
        rs = (cls.query.join(Order, cls.id == Order.user_id)
              .add_columns(cls.id, Order.id, cls.username, cls.phone_number, cls.email, Order.total, Order.voucher,
                           Order.tax).all())
        return rs


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
    order_detail = relationship("Order_detail", cascade="all, delete")
    recipe = relationship("Recipe", cascade="all, delete")

    def json(self):
        return {'id': self.id, 'name': self.name, 'price': self.price, 'product_detail': self.product_detail,
                'size': self.size, 'subcategory_id': self.subcategory_id}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_item(cls):
        rs = (cls.query.join(Subcategory, Subcategory.id == cls.subcategory_id)
              .join(Category, Category.id == Subcategory.category_id)
              .add_columns(cls.id, cls.name, cls.price, cls.product_detail, cls.size, Subcategory.id, Subcategory.name,
                           Category.id, Category.name)).all()
        return rs

    @classmethod
    def get_by_id_subcategory(cls, _id):
        return cls.query.filter_by(subcategory_id=_id).all()

    @classmethod
    def get_by_id_recipe(cls, _id):
        return cls.query.filter_by(recipe_id=_id).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def delete_by_id(cls, _id):
        rs = cls.query.filter_by(id=_id).first().order_detail
        return rs


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.String(100), primary_key=True)
    direction = db.Column(db.String(255))
    ingredient = db.Column(db.String(255))
    publish_at = db.Column(db.Integer, nullable=False)
    item_id = db.Column(ForeignKey(Item.id), nullable=False)

    def json(self):
        return {'id': self.id, 'direction': self.direction, 'ingredient': self.ingredient,
                'publish_at': self.publish_at, 'item_id': self.item_id}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_all_recipes(cls):
        rs = (cls.query.join(Item, Item.id == cls.item_id)
              .join(Subcategory, Subcategory.id == Item.subcategory_id)
              .join(Category, Category.id == Subcategory.category_id)
              .add_columns(cls.id, Item.name, cls.publish_at, Category.id, Category.name, Subcategory.id,
                           Subcategory.name)).all()
        return rs


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.String(100), primary_key=True)
    total = db.Column(db.Float, nullable=False)
    created_date = db.Column(db.Integer)
    status = db.Column(db.String(100), nullable=False)
    voucher = db.Column(db.String(50))
    tax = db.Column(db.String(50))
    user_id = db.Column(ForeignKey(User.id), nullable=False)
    make_invoice = db.Column(db.Boolean(), nullable=False)
    order_detail = relationship("Order_detail", cascade="all, delete")

    def json(self):
        return {'id': self.id, 'total': self.total, 'created_date': self.created_date,
                'status': self.status, 'voucher': self.voucher, 'tax': self.user_id, 'make_invoice': self.make_invoice,
                'user_id': self.user_id}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def delete_by_id(cls, _id):
        rs = cls.query.filter_by(id=_id).first().order_detail
        return rs


class Order_detail(db.Model):
    __tablename__ = 'orders_details'

    id = db.Column(db.String(100), primary_key=True)
    order_id = db.Column(ForeignKey(Order.id), nullable=False)
    item_id = db.Column(ForeignKey(Item.id), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    def json(self):
        return {'id': self.id, 'order_id': self.order_id, 'item_id': self.item_id, 'amount': self.amount}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_item_id(cls, _id):
        return cls.query.filter_by(item_id=_id).first()


class Image_item(db.Model):
    __tablename__ = 'images_item'

    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))
    item_id = db.Column(ForeignKey(Item.id), nullable=False)

    def json(self):
        return {'id': self.id, 'name': self.name, 'item_id': self.item_id}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id_item(cls, _id):
        return cls.query.filter_by(item_id=_id).all()


class Image_recipe(db.Model):
    __tablename__ = 'images_recipe'

    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))
    recipe_id = db.Column(ForeignKey(Recipe.id), nullable=False)

    def json(self):
        return {'id': self.id, 'name': self.name, 'recipe_id': self.recipe_id}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id_recipe(cls, _id):
        return cls.query.filter_by(recipe_id=_id).all()

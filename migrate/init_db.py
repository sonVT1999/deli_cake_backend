import json

from flask import Flask

from app.extensions import db
from app.models import User, Order_detail, Order, Recipe, Subcategory, Category, Image, Item
from app.settings import DevConfig

CONFIG = DevConfig
default_file = "default.json"


class Worker:
    def __init__(self):
        app = Flask(__name__)

        app.config.from_object(CONFIG)
        db.app = app
        db.init_app(app)
        app_context = app.app_context()
        app_context.push()

        print("=" * 25, f"Starting migrate database on the uri: {CONFIG.SQLALCHEMY_DATABASE_URI}", "=" * 25)
        db.drop_all()  # drop all tables
        db.create_all()  # create a new schema

        with open(default_file, encoding='utf-8') as file:
            self.default_data = json.load(file)

    def insert_default_users(self):
        users = self.default_data.get('users', {})
        for item in users:
            instance = User()
            for key in item.keys():
                instance.__setattr__(key, item[key])
            db.session.add(instance)
        db.session.commit()

    def insert_default_recipes(self):
        recipes = self.default_data.get('recipes', {})
        for item in recipes:
            instance = Recipe()
            for key in item.keys():
                instance.__setattr__(key, item[key])
            db.session.add(instance)
        db.session.commit()

    def insert_default_categories(self):
        categories = self.default_data.get('categories', {})
        for item in categories:
            instance = Category()
            for key in item.keys():
                instance.__setattr__(key, item[key])
            db.session.add(instance)
        db.session.commit()

    def insert_default_subcategories(self):
        subcategories = self.default_data.get('subcategories', {})
        for item in subcategories:
            instance = Subcategory()
            for key in item.keys():
                instance.__setattr__(key, item[key])
            db.session.add(instance)
        db.session.commit()

    def insert_default_items(self):
        items = self.default_data.get('items', {})
        for item in items:
            instance = Item()
            for key in item.keys():
                instance.__setattr__(key, item[key])
            db.session.add(instance)
        db.session.commit()

    def insert_default_orders(self):
        orders = self.default_data.get('orders', {})
        for item in orders:
            instance = Order()
            for key in item.keys():
                instance.__setattr__(key, item[key])
            db.session.add(instance)
        db.session.commit()

    def insert_default_order_details(self):
        order_details = self.default_data.get('order_details', {})
        for item in order_details:
            instance = Order_detail()
            for key in item.keys():
                instance.__setattr__(key, item[key])
            db.session.add(instance)
        db.session.commit()

    def insert_default_images(self):
        images = self.default_data.get('images', {})
        for item in images:
            instance = Image()
            for key in item.keys():
                instance.__setattr__(key, item[key])
            db.session.add(instance)
        db.session.commit()


if __name__ == '__main__':
    worker = Worker()
    worker.insert_default_users()
    worker.insert_default_categories()
    worker.insert_default_subcategories()
    worker.insert_default_items()
    worker.insert_default_recipes()
    worker.insert_default_orders()
    worker.insert_default_order_details()
    print("=" * 50, "Database migration completed", "=" * 50)

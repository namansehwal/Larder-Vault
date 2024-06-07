# backend/app/models.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import time

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")
    is_approved = db.Column(db.Boolean, default=1)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "is_approved": self.is_approved,
        }


class TokenBlacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.String(60))
    image = db.Column("image", db.String(60))
    date = db.Column("date", db.String(60))
    created_by = db.Column("created_by", db.Integer)
    is_approved = db.Column("is_approved", db.Boolean, default=1)

    def __init__(self, name, image, created_by, is_approved=1):
        name = name.rstrip()
        self.name = name
        self.image = image
        self.created_by = created_by
        self.is_approved = is_approved
        self.date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

   


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.String(60))
    image = db.Column("image", db.String(60))
    category_id = db.Column("category_id", db.Integer)
    price = db.Column("price", db.Integer)
    quantity = db.Column("quantity", db.Integer)
    time = db.Column("time", db.Integer)
    si_unit = db.Column("si_unit", db.Integer)
    best_before = db.Column("best_before", db.String(60))
    created_by = db.Column("created_by", db.Integer)
    is_approved = db.Column("is_approved", db.Boolean, default=1)

    def __init__(
        self,
        name,
        image,
        category_id,
        price,
        quantity,
        si_unit,
        best_before,
        created_by,
        is_approved=1,
    ):
        self.name = name
        self.image = image
        self.category_id = category_id
        self.price = price
        self.quantity = quantity
        self.si_unit = si_unit
        self.best_before = best_before
        self.created_by = created_by
        self.is_approved = is_approved
        self.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# create sample Product for testing


class Cart(db.Model):
    __tablename__ = "cart"
    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column("user_id", db.Integer)
    product_id = db.Column("product_id", db.Integer)
    product_name = db.Column("product_name", db.String(60))
    quantity = db.Column("quantity", db.Integer)
    price = db.Column("price", db.Integer)
    created_at = db.Column("created_at", db.String(60))

    def __init__(self, user_id, product_id, quantity, price, product_name):
        self.user_id = user_id
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.price = price
        self.created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def serialize(self):
        return {
            "cart_id": self.cart_id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "price": self.price,
            "created_at": self.created_at,
        }


class Order_Items(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column("user_id", db.Integer)
    order_id = db.Column("order_id", db.Integer)
    product_id = db.Column("product_id", db.Integer)
    product_name = db.Column("product_name", db.String(60))
    product_price = db.Column("product_price", db.Integer)
    quantity = db.Column("quantity", db.Integer)
    amount = db.Column("amount", db.Integer)
    created_at = db.Column("created_at", db.String(60))

    def __init__(
        self,
        user_id,
        order_id,
        product_id,
        quantity,
        price,
        product_name,
        product_price,
    ):
        self.user_id = user_id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.amount = price * quantity
        self.product_name = product_name
        self.product_price = product_price
        self.created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "product_price": self.product_price,
            "quantity": self.quantity,
            "amount": self.amount,
            "created_at": self.created_at,
        }


class Order_Detail(db.Model):
    __tablename__ = "order_detail"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column("user_id", db.Integer)
    total = db.Column("total", db.Integer)
    coupon_code = db.Column("coupon_code", db.String(60))
    discount_percentage = db.Column("discount_percentage", db.Integer)
    created_at = db.Column("created_at", db.String(60))

    def __init__(self, user_id, total, coupon_code=None, discount_percentage=None):
        self.user_id = user_id
        self.total = total
        self.coupon_code = coupon_code
        self.discount_percentage = discount_percentage
        self.created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

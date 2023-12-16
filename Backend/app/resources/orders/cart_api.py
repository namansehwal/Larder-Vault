from flask_restful import Resource
from flask import request
from app.models.model import db, Cart
from flask_jwt_extended import get_jwt_identity
from app.resources.auth.user_api import custom_jwt_required


class CartAPI(Resource):
    secured = custom_jwt_required()

    # @secured
    def get(self, user_id=None):
        if user_id:
            cart = Cart.query.filter_by(user_id=user_id).all()
            return {"cart": [c.serialize() for c in cart]}, 200
        else:
            return {"message": "User not found"}, 404

    # @secured
    def post(self, user_id=None):
        if user_id:
            data = request.get_json()
            check = Cart.query.filter_by(
                user_id=user_id, product_id=data["product_id"]
            ).first()
            if check:
                check.quantity += data["quantity"]
                db.session.commit()
                return {"message": "Cart updated"}, 200
            cart = Cart(
                user_id=user_id,
                product_id=data["product_id"],
                quantity=data["quantity"],
                product_name=data["product_name"],
                price=data["price"],
            )
            db.session.add(cart)
            db.session.commit()
            print(data["price"])
            return {"message": "Cart created"}, 201

    # @secured
    def delete(self, user_id=None):
        cart_id = user_id
        if cart_id:
            cart = Cart.query.filter_by(cart_id=cart_id).first()
            if cart:
                db.session.delete(cart)
                db.session.commit()
                return {"message": "Cart deleted"}, 200
            else:
                return {"message": "Cart not found"}, 404

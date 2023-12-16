from flask_restful import Resource
from flask import request
from app.models.model import db, Order_Items, Order_Detail, Cart, Product
from flask_jwt_extended import get_jwt_identity
from app.resources.auth.user_api import custom_jwt_required
import time
from app import app
from app.cache.cache import cache


class OrderAPI(Resource):
    secured = custom_jwt_required()

    # @secured
    def get(self, user_id=None):
        if user_id:
            orders = Order_Items.query.filter_by(user_id=user_id).all()
            return {"orders": [order.serialize() for order in orders]}, 200
        else:
            return {"message": "User not found"}, 404

    # @secured
    def post(self, user_id=None):
        if user_id:
            cache.clear()
            # Fetch cart items for the user

            cart_items = Cart.query.filter_by(user_id=user_id).all()

            if not cart_items:
                return {"message": "Cart is empty, order not placed"}, 400

            # Calculate total amount without coupon
            total_amount_without_coupon = sum(
                [cart_item.price * cart_item.quantity for cart_item in cart_items]
            )

            # Apply coupon code if provided in the request
            coupon_code = request.json.get("coupon_code")
            discount_percentage = 0

            if coupon_code in [
                "ECOMART10",
                "ECOMART25",
                "ECOMART50",
            ]:
                discount_percentage = int(coupon_code[-2:])

            # Calculate total amount after applying the discount
            total_amount_with_coupon = total_amount_without_coupon * (
                1 - discount_percentage / 100
            )

            # Create Order_Detail
            order_detail = Order_Detail(
                user_id=user_id,
                total=total_amount_with_coupon,
                coupon_code=coupon_code,
                discount_percentage=discount_percentage,
            )
            db.session.add(order_detail)
            db.session.commit()

            order_id = (
                order_detail.id
            )  # Assuming you have an 'id' field in Order_Detail

            # Create Order_Items for each cart item
            for cart_item in cart_items:
                order_item = Order_Items(
                    user_id=user_id,
                    order_id=order_id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    price=cart_item.price,
                    product_name=cart_item.product_name,
                    product_price=cart_item.price,
                )
                db.session.add(order_item)

            # Empty the cart after placing the order
            Cart.query.filter_by(user_id=user_id).delete()
            db.session.commit()
            discount_message = (
                f"Discount of {discount_percentage}% applied"
                if discount_percentage
                else "No discount applied"
            )
            # Delete the product quantity from the database
            for cart_item in cart_items:
                product = Product.query.filter_by(id=cart_item.product_id).first()
                product.quantity -= cart_item.quantity
                db.session.commit()

            return {"message": f"Order Placed Successfully, \nWill be Delivered Soon \n{discount_message} "}, 201

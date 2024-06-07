from flask_restful import Resource
from flask import request
from app.models.model import Category, db, Product, Order_Detail, User, Order_Items
from flask_jwt_extended import get_jwt_identity
from app.resources.auth.user_api import custom_jwt_required
from sqlalchemy import and_, func
from app.cache.cache import cache
import random

class SummaryAPI(Resource):
    # @custom_jwt_required()
    # @cache.cached(timeout=30, query_string=True)
    def get(self):
        result = {}

        # total sales
        total_sales = sum(order.total for order in Order_Detail.query.all())

        # total earnings
        total_earnings = round(total_sales * 0.25)

        # total users
        total_user = User.query.count()

        # total products
        total_products = Product.query.count()
        out_of_stock = Product.query.filter(Product.quantity < 1).count()

        # category-wise product counts
        category_data = []
        categories = Category.query.filter(Category.is_approved == True).all()
        for category in categories:
            category_name = category.name
            product_count = Product.query.filter(
                and_(Product.category_id == category.id, Product.quantity > 0)
            ).count()
            category_data.append(
                {"name": category_name, "product_count": product_count}
            )
        top_products_query = (db.session.query(
                                Order_Items.product_name, 
                                func.sum(Order_Items.quantity).label('total_sold')
                              )
                              .group_by(Order_Items.product_name)
                              .order_by(func.sum(Order_Items.quantity).desc())
                              .limit(10)
                              )
        top_products_list = top_products_query.all()
        random.shuffle(top_products_list)
        top_products = [
            {"name": item.product_name, "quantity": item.total_sold}
            for item in top_products_list
        ]
       
   
        

        # Set default values if not provided
        result = {
            "total_sales": total_sales,
            "total_earnings": total_earnings,
            "total_user": total_user,
            "total_products": total_products,
            "out_of_stock": out_of_stock,
            "categories": category_data,
            "top_products": top_products,
          
        }

       

        return result

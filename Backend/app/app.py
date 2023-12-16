# backend/app.py
from flask import Flask, jsonify, send_file
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config.config import Config
from app.models.model import db, bcrypt, User, Category
from app.cache.cache import cache


from app.resources.auth.admin_api import register_store_manager, approve_store_manager
from app.resources.products.category_api import CategoryAPI
from app.resources.products.product_api import ProductAPI
from app.resources.orders.summary_api import SummaryAPI
from app.resources.orders.cart_api import CartAPI
from app.resources.orders.order_api import OrderAPI
from app.resources.orders.request_api import RequestAPI

from app.resources.auth.user_api import (
    register_user,
    login,
    logout,
    custom_jwt_required as secured,
    user_details,
)
import time

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)
CORS(app)

CORS(
    app,
    resources={
        r"/*": {
            "origins": "http://localhost:5173",
            "supports_credentials": True,
            "Access-Control-Allow-Credentials": True,
        }
    },
)


# User registration and login endpoints
app.add_url_rule("/register/user", "register_user", register_user, methods=["POST"])
app.add_url_rule("/login", "login", login, methods=["POST"])
app.add_url_rule("/logout", "logout", secured()(logout), methods=["POST"])
app.add_url_rule("/user_details", "protected", secured()(user_details), methods=["GET"])

# Store Manager registration and approval endpoints
app.add_url_rule(
    "/register/store-manager",
    "register_store_manager",
    register_store_manager,
    methods=["POST"],
)
app.add_url_rule(
    "/approve/store-manager/<int:user_id>",
    "approve_store_manager",
    secured()(approve_store_manager),
    methods=["POST"],
)

# Category API endpoint
api = Api(app)
# add decorator to protect api endpoint
#add string is approved to category api
api.add_resource(CategoryAPI, "/category", "/category/<int:category_id>", "/category/<string:is_approved>")
api.add_resource(ProductAPI, "/product", "/product/<int:product_id>", "/product/<string:is_approved>")
api.add_resource(CartAPI, "/cart/<int:user_id>")
api.add_resource(OrderAPI, "/order/<int:user_id>")
api.add_resource(RequestAPI, "/requests/<int:user_id>", "/requests")
api.add_resource(SummaryAPI, "/summary")

from app.utils.tasks import store_manager_report, sm_report
from celery.result import AsyncResult

@app.get('/get-csv')
def get_csv(): 
    name = sm_report()
    time.sleep(2)    
    return send_file(name, as_attachment=True)

@app.get('/download-csv')
def download_csv():
    task = store_manager_report()
    return jsonify({"task_id": task}), 200



@app.get('/get-csv/<task_id>')
def get_csv_file(task_id):
    res = AsyncResult(task_id)
    if res.ready():
        filename = res.result
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({"message": "Task Pending"}), 404



# Create admin user if not exists
with app.app_context():
    db.create_all()
    admin_user = User.query.filter_by(username="admin").first()
    cache.init_app(app)

    if not admin_user:
        hashed_admin_password = bcrypt.generate_password_hash("admin").decode("utf-8")
        admin_user = User(
            username="admin",
            email="admin@admin.com",
            password=hashed_admin_password,
            role="admin",
            is_approved=True,
        )
        db.session.add(admin_user)
        db.session.commit()


from flask_restful import Resource
from flask import request
from app.models.model import Product, db, Category
from flask_jwt_extended import get_jwt_identity
from app.resources.auth.user_api import custom_jwt_required
from app.cache.cache import cache

class ProductAPI(Resource):
    secured = custom_jwt_required()

    def _get_product(self, product_id):
        return Product.query.get(product_id)

    def _is_authorized(self, required_role):
        return get_jwt_identity()["role"] == required_role

    def _handle_product_data(self, name, price, category_id, image, quantity, si_unit, best_before, created_by, is_approved=None):
        return Product(name=name, price=price, category_id=category_id, image=image, quantity=quantity, si_unit=si_unit, best_before=best_before, created_by=created_by, is_approved=is_approved)

    def _get_products(self, is_approved=None):
        if is_approved == 'pending':
            query = Product.query.filter(Product.created_by != "admin")
        else:
            query = Product.query.filter(Product.is_approved == True)    
        return query.all()

    @secured
    @cache.cached(timeout=300, query_string=True)
    def get(self, product_id=None, is_approved=None):
        if is_approved == "pending":
            products = self._get_products(is_approved)
            return {
                prod.id: {
                    "id": prod.id, "name": prod.name, "price": prod.price, "category_id": prod.category_id,
                    "image": prod.image, "quantity": prod.quantity, "si_unit": prod.si_unit, "best_before": prod.best_before,
                    "category_name": Category.query.get(prod.category_id).name if Category.query.get(prod.category_id) else "Unknown",
                    "created_by": prod.created_by
                }
                for prod in products
            }, 200

        if product_id:
            product = self._get_product(product_id)
            if product:
                return {"id": product.id, "name": product.name, "price": product.price, "category_id": product.category_id, "image": product.image, "quantity": product.quantity, "si_unit": product.si_unit, "best_before": product.best_before}, 200
            return {"message": "Product not found"}, 404

        products = self._get_products(is_approved=is_approved)
        return {
            prod.id: {
                "id": prod.id, "name": prod.name, "price": prod.price, "category_id": prod.category_id,
                "image": prod.image, "quantity": prod.quantity, "si_unit": prod.si_unit, "best_before": prod.best_before,
                "category_name": Category.query.get(prod.category_id).name if Category.query.get(prod.category_id) else "Unknown"
            }
            for prod in products
        }, 200

    @secured
    def post(self):
        cache.clear()
        role = get_jwt_identity()["role"]
        data = request.get_json()
        name, price, category_id, image, quantity, si_unit, best_before = data.get("name"), data.get("price"), data.get("category_id"), data.get("image"), data.get("quantity"), data.get("si_unit"), data.get("best_before")

        if role == "store-manager":
            created_by = f"{get_jwt_identity()['username']},create"
            product = self._handle_product_data(name, price, category_id, image, quantity, si_unit, best_before, created_by, is_approved=False)
            db.session.add(product)
            db.session.commit()
            return {"message": "Product created, pending approval"}, 201

        if role != "admin":
            return {"message": "Not authorized"}, 403

        created_by = data.get("created_by")
        is_approved = data.get("is_approved", True)
        product = self._handle_product_data(name, price, category_id, image, quantity, si_unit, best_before, created_by, is_approved)
        db.session.add(product)
        db.session.commit()
        return {"message": "Product created"}, 201

    @secured
    def put(self, product_id):
        cache.clear()
        product = self._get_product(product_id)
        if not product:
            return {"message": "Product not found"}, 404
        
        data = request.get_json()
        if self._is_authorized("store-manager"):
            created_by = f"{get_jwt_identity()['username']},update,{data.get('name')},{data.get('image')},{data.get('category_id')},{data.get('price')},{data.get('quantity')},{data.get('si_unit')},{data.get('best_before')}"
            self._update_product(product, created_by=created_by)
            return {"message": "Category update request captured, pending approval"}, 201

        data = request.get_json()
        if not self._is_authorized("admin"):
            return {"message": "Not authorized"}, 403

        self._update_product(product, **data)
        return {"message": "Product updated"}, 201

    def _update_product(self, product, **kwargs):
        for key, value in kwargs.items():
            if hasattr(product, key) and value is not None:
                setattr(product, key, value)
        db.session.commit() 

    @secured
    def delete(self, product_id):
        cache.clear()
        product = self._get_product(product_id)
        if not product:
            return {"message": "Product not found"}, 404
        
        if self._is_authorized("store-manager"):
            created_by = f"{get_jwt_identity()['username']},delete"
            self._update_product(product, created_by=created_by)
            return {"message": "Product deletion request captured, pending approval"}, 201

        if not self._is_authorized("admin"):
            return {"message": "Not authorized"}, 403

        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted"}, 201


# from flask_restful import Resource
# from flask import request
# from app.models.model import Product, db, Category
# from flask_jwt_extended import get_jwt_identity
# from app.resources.auth.user_api import custom_jwt_required
# from app.cache.cache import cache

# class ProductAPI(Resource):
#     secured = custom_jwt_required()

#     def _get_product(self, product_id):
#         return Product.query.get(product_id)

#     @secured
#     @cache.cached(timeout=300, query_string=True)
#     def get(self, product_id=None):   
#         if product_id:
#             product = self._get_product(product_id)
#             return {"data": product.serialize()} if product else {
#                 "message": "Product not found"
#             }, 200 if product else 404
#         else:
#             products = Product.query.all()

#             result_dic = {}
#             if products:
#                 for prod in products:
#                     result_dic[prod.id] = {
#                         "id": prod.id,
#                         "name": prod.name,
#                         "price": prod.price,
#                         "category_id": prod.category_id,
#                         "image": prod.image,
#                         "quantity": prod.quantity,
#                         "si_unit": prod.si_unit,
#                         "best_before": prod.best_before,
#                         "category_name": Category.query.get(prod.category_id).name
#                         if Category.query.get(prod.category_id)
#                         else "Unknown",
#                     }
#                 return result_dic, 200

#             else:
#                 return {"message": "No products found"}, 404

#     @secured
#     def post(self):
#         cache.clear()
#         if get_jwt_identity()["role"] != "admin":
#             return {"message": "Not authorized"}

#         data = request.get_json()
#         new_product = Product(**data)
#         db.session.add(new_product)
#         db.session.commit()
#         return {"message": "Product created successfully"}, 201

#     @secured
#     def put(self, product_id):
#         cache.clear()
#         if get_jwt_identity()["role"] != "admin":
#             return {"message": "Not authorized"}

#         product = self._get_product(product_id)
#         if product:
#             data = request.get_json()
#             for key, value in data.items():
#                 setattr(product, key, value)
#             db.session.commit()
#             return {"message": "Product updated successfully"}, 201
#         else:
#             return {"message": "Product not found"}, 404

#     @secured
#     def delete(self, product_id):
#         #clear cache
#         cache.clear()
#         if get_jwt_identity()["role"] != "admin":
#             return {"message": "Not authorized"}

#         product = self._get_product(product_id)
#         if product:
#             db.session.delete(product)
#             db.session.commit()
#             return {"message": "Product deleted successfully"}, 201
#         else:
#             return {"message": "Product not found"}, 404

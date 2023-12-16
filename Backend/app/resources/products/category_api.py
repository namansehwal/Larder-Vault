from flask_restful import Resource
from flask import request
from app.models.model import Category, db, Product
from flask_jwt_extended import get_jwt_identity
from app.resources.auth.user_api import custom_jwt_required
from app.cache.cache import cache

class CategoryAPI(Resource):
    secured = custom_jwt_required()

    def _get_category(self, category_id):
        return Category.query.get(category_id)

    def _is_authorized(self, required_role):
        return get_jwt_identity()["role"] == required_role

    def _handle_category_data(self, name, image, created_by, is_approved=None):
        return Category(name=name, image=image, created_by=created_by, is_approved=is_approved)

    def _get_categories(self, is_approved=None):
        
        if is_approved == 'pending':
            #check filter created_by not equal to admin
             print("is_approved", is_approved)
             query = Category.query.filter(Category.created_by != "admin")
        else:
            query = Category.query.filter(Category.is_approved == True)   
        return query.all()

    @secured
    @cache.cached(timeout=300, query_string=True)
    def get(self, category_id=None, is_approved=None):
        if is_approved == "pending":
            categories = self._get_categories(is_approved)
            return {
                cat.id: {"id": cat.id, "name": cat.name, "image": cat.image, "created_by": cat.created_by}
                for cat in categories
            }

        if category_id:
            category = self._get_category(category_id)
            if category:
                return {"id": category.id, "name": category.name, "image": category.image}, 200
            return {"message": "Category not found"}, 404

        categories = self._get_categories()
        return {
            cat.id: {"id": cat.id, "name": cat.name, "image": cat.image}
            for cat in categories
        }
        

    @secured
    def post(self):
        cache.clear()
        role = get_jwt_identity()["role"]
        data = request.get_json()
        name, image = data.get("name"), data.get("image")

        if role == "store-manager":
            created_by = f"{get_jwt_identity()['username']},create"
            category = self._handle_category_data(name, image, created_by, is_approved=False)
            db.session.add(category)
            db.session.commit()
            return {"message": "Category created, pending approval"}, 201

        if role != "admin":
            return {"message": "Not authorized"}, 403

        created_by = data.get("created_by")
        is_approved = data.get("is_approved", True)
        category = self._handle_category_data(name, image, created_by, is_approved)
        db.session.add(category)
        db.session.commit()
        return {"message": "Category created"}, 201

    @secured
    def put(self, category_id):
        cache.clear()
        category = self._get_category(category_id)
        if not category:
            return {"message": "Category not found"}, 404

        data = request.get_json()
        if self._is_authorized("store-manager"):
            created_by = f"{get_jwt_identity()['username']}, update,{data.get('name')},{data.get('image')}"
            self._update_category(category, created_by=created_by)
            return {"message": "Category update request captured, pending approval"}, 201

        if not self._is_authorized("admin"):
            return {"message": "Not authorized"}, 403

        self._update_category(category, **data)
        return {"message": "Category updated"}, 201

    def _update_category(self, category, **kwargs):
        for key, value in kwargs.items():
            if hasattr(category, key) and value is not None:
                setattr(category, key, value)
        db.session.commit()

    @secured
    def delete(self, category_id):
        cache.clear()
        category = self._get_category(category_id)
        if not category:
            return {"message": "Category not found"}, 404

        if self._is_authorized("store-manager"):
            created_by = f"{get_jwt_identity()['username']}, delete"
            self._update_category(category, created_by=created_by)
            return {"message": "Category deletion request captured, pending approval"}, 201

        if not self._is_authorized("admin"):
            return {"message": "Not authorized"}, 403

        # Delete all products in this category
        Product.query.filter_by(category_id=category_id).delete()
        db.session.delete(category)
        db.session.commit()
        return {"message": "Category deleted"}, 201



# backend/app/resources/auth/user_api.py
from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
from flask_jwt_extended.exceptions import JWTDecodeError
from app.models.model import db, bcrypt, User, TokenBlacklist


def register_user():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user:
        return jsonify({"message": "User already exists."}), 400

    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    new_user = User(
        username=data["username"],
        email=data["email"],
        password=hashed_password,
        role="user",
        is_approved=True,
    )
    db.session.add(new_user)
    db.session.commit()
    return (
        jsonify({"message": "User registered successfully!\nLogin To Continue."}),
        201,
    )


def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user:
        if user.is_approved == False:
            return (
                jsonify(
                    {
                        "message": f'Store_Manager "{user.username}" \nPending For Approval by Admin.'
                    }
                ),
                401,
            )

    if user and bcrypt.check_password_hash(user.password, data["password"]):
        access_token = create_access_token(
            identity={"username": user.username, "email": user.email, "role": user.role}
        )
        # add message to response
        return (
            jsonify(access_token=access_token, message=f"Welcome {user.username}!"),
            200,
        )
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Invalid, Wrong credentials entered!!!"}), 401


def logout():
    jti = get_jwt()["jti"]
    token_in_blacklist = TokenBlacklist.query.filter_by(token=jti).first()
    if token_in_blacklist:
        return jsonify({"message": "Token already revoked"}), 200

    db.session.add(TokenBlacklist(token=jti))
    db.session.commit()
    return jsonify({"message": "Logout successful"}), 200


def custom_jwt_required():
    def decorator(fn):
        @jwt_required()
        def wrapper(*args, **kwargs):
            try:
                jti = get_jwt()["jti"]
                token_in_blacklist = TokenBlacklist.query.filter_by(token=jti).first()
                if token_in_blacklist:
                    return jsonify({"message": "Token has been revoked"}), 401
                return fn(*args, **kwargs)
            except JWTDecodeError:
                return jsonify({"message": "Invalid token"}), 401

        return wrapper

    return decorator


def user_details():
    current_user = get_jwt_identity()
    # add user id to jwt_identity
    current_user["id"] = (
        User.query.filter_by(username=current_user["username"]).first().id
    )

    return jsonify(logged_in_as=current_user), 200

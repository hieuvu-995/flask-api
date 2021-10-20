from typing import Optional
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from app.models.user import UserModel
from app.blacklist import BLACKLIST

_parser = reqparse.RequestParser()
_parser.add_argument(
    "username", type=str, required=True, help="This field cannot be blank"
)
_parser.add_argument(
    "password", type=str, required=True, help="This field cannot be blank"
)


class UserRegister(Resource):
    @classmethod
    def post(cls):
        data = _parser.parse_args()
        if UserModel.find_by_name(data["username"]):
            return {"message": "username already exists"}, 400
        user = UserModel(data["username"], data["password"])
        user.save_to_db()
        return {"message": "create user successfully!"}, 200


class User(Resource):
    @classmethod
    def get(cls, username):
        user = UserModel.find_by_name(username)
        if user:
            return user.json()
        return {"message": "user not found"}

    @classmethod
    def delete(cls, username):
        user = UserModel.find_by_name(username)
        user.delete_from_db()
        return {"message": "user has been deleted"}

    @jwt_required()
    @classmethod
    def post(cls):
        data = _parser.parse_args()
        user = UserModel.find_by_name(data["username"])
        if user:
            user.password = data["password"]
            user.save_to_db()
            return {"message": "update successfully"}
        else:
            return {"message": "username not found"}


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _parser.parse_args()
        user = UserModel.find_by_name(data["username"])
        if user and user.password == data["password"]:
            additional_claims = {"claims": user.role}
            access_token = create_access_token(
                identity=data["username"],
                fresh=True,
                additional_claims=additional_claims,
            )
            refresh_token = create_refresh_token(identity=data["username"])
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        return {"message": "Invalid credentials"}, 400


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()["jti"]
        BLACKLIST.add(jti)
        return {"message": "Log out successfully"}


class RefreshToken(Resource):
    """
    Create new access token
    """

    @jwt_required(refresh=True)
    @classmethod
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200


class SetRole(Resource):
    """
    Set admin role to default account
    """

    @jwt_required()
    @classmethod
    def post(self, username):
        user = UserModel.find_by_name(username)
        if user:
            user.role = "admin"
            user.save_to_db()
            return {"message": "Set role successfully"}
        else:
            return {"message": "User not found"}

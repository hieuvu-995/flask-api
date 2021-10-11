from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jti
    )
from app.models.user import UserModel
from app.blacklist import BLACKLIST

_parser = reqparse.RequestParser()
_parser.add_argument(
    'username',
    type = str,
    required = True,
    help = 'This field cannot be blank'

)
_parser.add_argument(
    'password',
    type = str,
    required = True,
    help = 'This field cannot be blank'

)


class UserRegister(Resource):
    def post(self):
        data = _parser.parse_args()
        if UserModel.find_by_name(data['username']):
            return {'message' : 'username already exists'}, 400    
        user = UserModel(data['username'], data['password'])
        user.save_to_db()
        return {'message':'create user successfully!'}, 200

class User(Resource):
    def get(self, username):
        user = UserModel.find_by_name(username)
        if user:
            return user.json()
        return {'message':'user not found'}

    def delete(self, username):
        user = UserModel.find_by_name(username)
        user.delete_from_db()
        return {'message':'user has been deleted'}
        
    @jwt_required()
    def post(self):
        data = _parser.parse_args()
        user = UserModel.find_by_name(data['username'])
        if user:       
            user.password = data['password']
            user.save_to_db()
            return {'message':'update successfully'}
        else:
            return {'message' : 'username not found'}
class UserLogin(Resource):
    def post(self):
        data = _parser.parse_args()
        user = UserModel.find_by_name(data['username'])
        if user and user.password == data['password']:
            access_token = create_access_token(identity=data['username'], fresh = True)
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'access_token':access_token, 
                'refresh_token':refresh_token
            }, 200
        return {'message':'Invalid credentials'}, 400

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_jti()
        BLACKLIST.add(jti)
        return {'message' : 'Logout successfully'}
    
class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh = False)
        return {'access_token' : new_token}, 200

from flask_jwt_extended.utils import get_jwt
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource, reqparse

from app.models.store import StoreModel

_parser = reqparse.RequestParser()
_parser.add_argument(
    'name',
    type = str,
    required = True,
    help = 'This field cannot be blank'
)

class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message' : 'store not found'}
    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message' : 'This store already exists'}
        new_store = StoreModel(name)
        try:
            new_store.save_to_db()
            return {'message' : 'Create store successfully'}
        except:
            {'message' : 'Error when create store'}
    
    def put(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            data = _parser.parse_args()
            store.name = data['name']
            try:
                store.save_to_db()
                return {'message':'Update successfully'}
            except:
                {'message':'Error when update'}
        return {'message':'Store not found'}

class StoreList(Resource):
    """
    Get store list
    """
    #Get full data if logged in. If not, only get 1 piece of data
    @jwt_required(optional=True)
    def get(self):
        confirm = get_jwt()
        store = [store.json() for store in StoreModel.find_all()]
        if confirm:
            return {'stores':store}
        return {
            'store' : store[0],
            'message' : 'Login for more information'
        }
        
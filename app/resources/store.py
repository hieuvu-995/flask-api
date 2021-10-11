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
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message' : 'store not found'}

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
    def get(self):
        return {'stores':[store.json() for store in StoreModel.find_all()]}
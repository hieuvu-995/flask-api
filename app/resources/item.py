from flask_restful import Resource, reqparse

from app.models.item import ItemModel


_parser = reqparse.RequestParser()
_parser.add_argument(
    'price',
    type=str,
    required = True,
    help='This field cannot be blank'
)
_parser.add_argument(
    'store_id',
    type = int,
    required = True,
    help = 'This field cannot be blank'
)

class Item(Resource):
    def post(self, name):
        data = _parser.parse_args()
        ItemModel.find_by_name(name)
        if data:
            item = ItemModel(name, data['price'], data['store_id'])
            item.save_to_db()
            return item.json()

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'}

    def put(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            data = _parser.parse_args()
            item.name = data['name']
            item.price = data['price']
            item.store_id = data['store_id']
            try:
                item.save_to_db()
                return {'message' : 'Update successfully'}
            except:
                return {'message' : 'Error when update'}
        return {'message' : 'Item not found'}
    
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        item.delete_from_db()
        return {'message' : 'Item deleted'}

class ItemList(Resource):
    def get(self):
        return {'items' : [item.json() for item in ItemModel.find_all()]}
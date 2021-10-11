from app import api
from app.resources.item import Item, ItemList
from app.resources.store import Store, StoreList
from app.resources.user import UserRegister, User, UserLogin, UserLogout, RefreshToken

api.add_resource(User,"/user/<string:name>")
api.add_resource(UserRegister,'/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores' )
api.add_resource(RefreshToken, '/refresh')


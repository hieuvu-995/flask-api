from app import db

class ItemModel(db.Model):
    __tablename__='items'
    id = db.Column(db.INTEGER, primary_key= True)
    name = db.Column(db.String(50), nullable = False, unique = True)
    price = db.Column(db.String(50), nullable = False)
    store_id = db.Column(db.Integer, foreign_key('stores.id')) 
    store = db.relationship('StoreModel', back_populates = 'items')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return  {'name': self.name, 'price':self.price, 'store_id':self.store_id}
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()
    

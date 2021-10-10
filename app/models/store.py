from app import db

class StoreModel(db.Model):
    __tablename__='stores'
    id = db.Column(db.INTEGER, primary_key= True)
    name = db.Column(db.String(50), nullable = False, unique = True)
    items = db.relationship('UserModel', back_populates = 'store', lazy = 'dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'store_name':self.name, 'items': [item.json() for item in self.items.all()]}
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, username):
        return cls.query.filter_by(username = username).first()
    
    @classmethod
    def find_all(cls, _id):
        return cls.query.all()
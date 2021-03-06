from app import db

class UserModel(db.Model):
    __tablename__='users'
    id = db.Column(db.INTEGER, primary_key= True)
    username = db.Column(db.String(50), nullable = False, unique = True)
    password = db.Column(db.String(50), nullable = False)
    role = db.Column(db.String(50))

    def __init__(self, username, password, role = 'user'):
        self.username = username
        self.password = password
        self.role = role

    def json(self):
        return  
    
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
    def find_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first()
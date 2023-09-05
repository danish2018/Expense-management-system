from flask_login import UserMixin
from .  import db





class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key =True , autoincrement=True)
    email = db.Column(db.String(60), unique = True)
    username= db.Column(db.String(20),unique = True)
    password = db.Column(db.String(40),unique = True)
    contact = db.Column(db.String(50),unique = True)
    is_admin = db.Column(db.Boolean , default = False)    
    expences = db.relationship('Expence',backref ='add_by',passive_deletes = True)


class Expence(db.Model):
    id = db.Column(db.Integer,primary_key =True , autoincrement=True)
    name = db.Column(db.String(60))
    date = db.Column(db.String(20))
    amount= db.Column(db.String(40))
    goods = db.Column(db.String(50))
    added_by = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    # user= db.relationship('User',backref ='expences',passive_deletes = True)


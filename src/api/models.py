from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    birthday = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    address = db.Column(db.String(300), unique=False, nullable=False)
    pedidos = db.relationship("Pedidos")

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active":self.is_active,
            "first_name":self.first_name,
            "last_name":self.last_name,
            "birthday":self.birthday,
            "phone":self.phone,
            "address":self.address
            # do not serialize the password, its a security breach
        }

class Platos(db.Model):
    __tablename__ = "Platos"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.String(250), unique=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<Platos {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price":self.price,
            "description":self.description,
            "is_active":self.is_active
            
        }

class Pedidos(db.Model):
    __tablename__ = "Pedidos"
    id = db.Column(db.Integer, primary_key=True)
    User_id = db.Column(db.Integer, ForeignKey("User.id"))
    Platos_id = db.Column(db.Integer, ForeignKey("Platos.id"))

    def __repr__(self):
        return f'<Pedidos {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "User_id": self.User_id,
            "Platos_id": self.Platos_id
        }
    
#class DetallesDePedidos(db.Model):
 #  __tablename__ = ""
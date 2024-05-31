from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    #Atributos
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    first_name = db.Column(db.String(), unique=False, nullable=True)
    last_name = db.Column (db.String(), unique=False, nullable=True)

    def __repr__(self):
        return f'<User: {self.email}>'

    def serialize(self):
        # do not serialize the password, its a security breach
        return {"id": self.id,
                "email": self.email,
                "is_active": self.is_active,
                "first_name": self.first_name,
                "last_name": self.last_name}

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user_to = db.relationship("Users", foreign_keys=[user_id])
    description = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    publication_date = db.Column(db.Date)
    image_url = db.Column (db.String)

    
    def __repr__(self):
        return f'<Post: {self.title}>'

    def serialize(self):
        # do not serialize the password, its a security breach
        return {"id": self.id,
                "title": self.title,
                "user_id": self.user_id,
                "description": self.description,
                "body": self.body,
                "publication_date": self.publication_date,
                "image_url": self.image_url
                }

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    comment_date = db.Column(db.Date)
    post_id = db.Column (db.Integer, db.ForeignKey("posts.id"))
    comment_to = db.relationship("Posts", foreign_keys=[post_id])
    author_id = db.Column (db.Integer, db.ForeignKey("users.id"))
    author = db.relationship("Users", foreign_keys=[author_id])

    
    def __repr__(self):
        return f'<Comment: {self.title}>'

    def serialize(self):
        # do not serialize the password, its a security breach
        return {"id": self.id,
                "body": self.body,
                "comment_date": self.comment_date,
                "post_id": self.post_id,
                "author_id": self.author_id
                
                }




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

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    diameter = db.Column(db.Float)

    def __repr__(self):
        return f'<Planet: {self.name}>'

    def serialize(self):
        # do not serialize the password, its a security breach
        return {"id": self.id,
                "name": self.name,
                "diameter": self.diameter,
                }

class Characters(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    home_world = db.Column(db.ForeignKey("planets.id"))
    world = db.relationship("Planets", foreign_keys=[home_world])

    def __repr__(self):
        return f'<Character: {self.name}>'

    def serialize(self):
        # do not serialize the password, its a security breach
        return {"id": self.id,
                "name": self.name,
                "description": self.description,
                "home_world": self.home_world,
                }

class Films(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    release = db.Column(db.Date, nullable=False)
    director = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return f'<Film: {self.name}>'

    def serialize(self):
        # do not serialize the password, its a security breach
        return {"id": self.id,
                "name": self.name,
                "release": self.release,
                "director": self.director
                }

class CharactersFilms(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String, nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"), nullable=False)
    character_to = db.relationship("Characters", foreign_keys=[character_id])
    film_id = db.Column(db.Integer, db.ForeignKey("films.id"), nullable=False)
    film_to = db.relationship("Films", foreign_keys=[film_id])

    def __repr__(self):
        return f'<Character film: {self.name}>'
    

    def serialize(self):
        # do not serialize the password, its a security breach
        return {"id": self.id,
                "role": self.role,
                "character_id": self.character_id,
                "film_id": self.film_id
                }

class Follower(db.Model): 

    id = db.Column(db.Integer, primary_key=True)
    user_from_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user_from_to = db.relationship("Users", foreign_keys=[user_from_id])
    user_to_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user_to_to = db.relationship("Users", foreign_keys=[user_to_id])
    
    def serialize(self):
        # do not serialize the password, its a security breach
        return {"user_from_id": self.user_to_id,
                "user_to_id": self.user_to_id,
                } 

class PlanetFavorites(db.Model): 

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user_to = db.relationship("Users", foreign_keys=[user_id])
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"), nullable=False)
    planet_to = db.relationship("Planets", foreign_keys=[planet_id])
    
    def serialize(self):
        # do not serialize the password, its a security breach
        return {"id": self.id,
                "user_id": self.tipe,
                "planet_id": self.post_id
                }   

class CharacterFavorites(db.Model): 

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user_to = db.relationship("Users", foreign_keys=[user_id])
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"), nullable=False)
    character_to = db.relationship("Characters", foreign_keys=[character_id])
    
    def serialize(self):
        # do not serialize the password, its a security breach
        return {"id": self.id,
                "user_id": self.tipe,
                "character_id": self.post_id
                }               


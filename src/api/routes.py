"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from datetime import datetime
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from api.models import db, Users, Posts, Comments, Characters, Planets

api = Blueprint('api', __name__)
CORS(api)# Allow CORS requests to this API


#Ruta para el login, esto me genera un token para la sesión si el usuario y contraseña coinciden
@api.route("/login", methods=["POST"])
def login():
    response_body={}
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    first_name = request.json.get("name", None)
    #Logica validacion usuario y contraseña
    user = db.session.execute(db.select(Users).where(Users.email == email, Users.password == password, Users.is_active == True)).scalar()
    if user:
        access_token = create_access_token(identity={"user_id" :user.id, "user_is_admin" : user.is_admin})
        response_body["message"] = "User Logeado"
        response_body["access_token"] = access_token
        response_body["results"] = user.serialize()
        return response_body, 200
    response_body['message'] = 'Bad username or password'
    return response_body, 401

# Protect a route with jwt_required, which will kick out requests
@api.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    response_body={}
    current_user = get_jwt_identity()
    response_body["message"]= f'User logueado:{current_user}'
    # Access the identity of the current user with get_jwt_identity
    return response_body, 200

@api.route('/signup', methods=['POST'])
def signup():
    response_body = {}
    email = request.json.get("email", None).lower()
    password = request.json.get("password", None)
    first_name = request.json.get("first_name", None)
    last_name = request.json.get("last_name", None)
    # Logica de verificación de un mail válido y password válido
    user = Users()
    user.email = email
    user.password = password
    user.first_name = first_name
    user.last_name = last_name
    user.is_active = True
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(identity={'user_id': user.id,
                                                 'user_is_admin': user.is_admin})
    response_body['message'] = 'User Registrado y logeado'
    response_body['access_token'] = access_token
    return response_body, 200

# Rutas para mi pestaña USERS
@api.route('/users', methods=['GET', 'POST'])
def handle_users():
    response_body={}
    if request.method == 'GET':
        users = db.session.execute(db.select(Users)).scalars()
        results = [row.serialize() for row in users]
        response_body['results'] = results
        response_body['message'] = "Users List"
        return response_body, 200
    if request.method == 'POST':
        response_body['message'] = "Not valid endpoint, must LOGIN"
        return response_body, 200


@api.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(user_id):
    response_body = {}
    if request.method == 'GET':
        user = db.session.execute(db.select(Users).where(Users.id == user_id)).scalar()
        if user:
            response_body['results'] = user.serialize()
            response_body['message'] = 'Usuario encontrado'
            return response_body, 200
        response_body['message'] = 'Usario inexistente'
        response_body['results'] = {}
        return response_body, 404
    if request.method == 'PUT':
        data = request.json
        user = db.session.execute(db.select(Users).where(Users.id == user_id)).scalar()
        if user:
            user.email = data['email']
            user.is_active = data['is_active']
            user.last_name = data['last_name']
            user.first_name = data['first_name']
            db.session.commit()
            response_body['message'] = 'Datos del usuario actualizados'
            response_body['results'] = user.serialize()
            return response_body, 200
        response_body['message'] = 'Usario inexistente'
        response_body['results'] = {}
        return response_body, 404
    if request.method == 'DELETE':
        user = db.session.execute(db.select(Users).where(Users.id == user_id)).scalar()
        if user:
            db.session.delete(user)
            user.is_active = False
            db.session.commit()
            response_body['message'] = 'Usuario eliminado'
            response_body['results'] = {}
        response_body['message'] = 'Usuario inexistente'
        response_body['results'] = {}
        return response_body, 200

#Rutas para mi pestaña POSTS
@api.route('/posts', methods=['GET', 'POST'])
@jwt_required()
def handle_posts():
    response_body={}
    current_user = get_jwt_identity()
    if request.method == 'GET':
        posts = db.session.execute(db.select(Posts)).scalars()
        results = [row.serialize() for row in posts]
        response_body['results'] = results
        response_body['message'] = "Posts List"
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        row = Posts()
        row.title = data['title']
        row.description = data['description']
        row.body = data['body']
        row.image_url = data['image_url']
        row.publication_date = datetime.today()
        row.user_id = current_user['user_id']
        db.session.add(row)
        db.session.commit()
        response_body['results'] = row.serialize()
        response_body['message'] = 'Post created'
        return response_body, 200


@api.route('/posts/<int:post_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_post(post_id):
    response_body = {}
    if request.method == 'GET':
        post = db.session.execute(db.select(Posts).where(Posts.id == post_id)).scalar()
        if post:
            response_body['results'] = post.serialize()
            response_body['message'] = 'Post encontrado'
            return response_body, 200
        response_body['message'] = 'Post inexistente'
        response_body['results'] = {}
        return response_body, 404
    if request.method == 'PUT':
        data = request.json
        post = db.session.execute(db.select(Posts).where(Posts.id == post_id)).scalar()
        if post:
            post.title = data['title']
            post.description = data['description']
            post.body = data['body']
            post.date = data['date']
            post.image_url = data['image_url']
            db.session.commit()
            response_body['message'] = 'Post actualizado'
            response_body['results'] = post.serialize()
            return response_body, 200
        response_body['message'] = 'Post inexistente'
        response_body['results'] = {}
        return response_body, 404
    if request.method == 'DELETE':
        post = db.session.execute(db.select(Posts).where(Posts.id == post_id)).scalar()
        if post:
            db.session.delete(post)
            db.session.commit()
            response_body['message'] = 'Post deleted'
            response_body['results'] = {}
        response_body['message'] = 'Post deleted'
        response_body['results'] = {}
        return response_body, 200


#Rutas para mi pestaña Comments
@api.route('/comments', methods=['GET', 'POST'])
@jwt_required()
def handle_comments():
    response_body={}
    current_user = get_jwt_identity()
    if request.method == 'GET':
        comments = db.session.execute(db.select(Comments)).scalars()
        results = [row.serialize() for row in comments]
        response_body['results'] = results
        response_body['message'] = "Comments List"
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        row = Comments()
        row.body = data['body']
        row.comment_date = datetime.today()
        row.author_id = current_user['user_id']
        row.post_id = data['post_id'] #Preguntar para que lo asigne automático
        db.session.add(row)
        db.session.commit()
        response_body['results'] = row.serialize()
        response_body['message'] = 'Post created'
        return response_body, 200

@api.route('/comments/<int:comment_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_comment(comment_id):
    response_body = {}
    if request.method == 'GET':
        comment = db.session.execute(db.select(Comments).where(Comments.id == comment_id)).scalar()
        if comment:
            response_body['results'] = comment.serialize()
            response_body['message'] = 'Comment found'
            return response_body, 200
        response_body['message'] = 'Comment not found'
        response_body['results'] = {}
        return response_body, 404
    if request.method == 'PUT':
        data = request.json
        comment = db.session.execute(db.select(Comments).where(Comments.id == comment_id)).scalar()
        if comment:
            comment.body = data['body']
            comment.date = data['date']
            db.session.commit()
            response_body['message'] = 'Comment update'
            response_body['results'] = comment.serialize()
            return response_body, 200
        response_body['message'] = 'Comment not found'
        response_body['results'] = {}
        return response_body, 404
    if request.method == 'DELETE':
        comment = db.session.execute(db.select(Comments).where(Comments.id == comment_id)).scalar()
        if comment:
            db.session.delete(comment)
            db.session.commit()
            response_body['message'] = 'Comment deleted'
            response_body['results'] = {}
        response_body['message'] = 'Comment deleted'
        response_body['results'] = {}
        return response_body, 200


#Lógica para la pestaña Characters
@api.route('/characters', methods=['GET', 'POST'])
def handle_characters():
    response_body={}
    if request.method == 'GET':
        characters = db.session.execute(db.select(Characters)).scalars()
        results = [row.serialize() for row in characters]
        response_body['results'] = results
        response_body['message'] = "Characters List"
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        row = Characters()
        row.name = data['name']
        row.description = data['description']
        row.home_world = data['home_world'] #Preguntar
        db.session.add(row)
        db.session.commit()
        response_body['results'] = row.serialize()
        response_body['message'] = 'Character created'
        return response_body, 200


@api.route('/characters/<int:character_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_character(character_id):
    response_body = {}
    if request.method == 'GET':
        character = db.session.execute(db.select(Characters).where(Characters.id == character_id)).scalar()
        if character:
            response_body['results'] = character.serialize()
            response_body['message'] = 'Character found'
            return response_body, 200
        response_body['message'] = 'Character not found'
        response_body['results'] = {}
        return response_body, 404
    if request.method == 'PUT':
        data = request.json
        character = db.session.execute(db.select(Characters).where(Characters.id == character_id)).scalar()
        if character:
            character.name = data['name']
            character.description = data['description']
            character.home_world = data['home_world']
            db.session.commit()
            response_body['message'] = 'Character update'
            response_body['results'] = character.serialize()
            return response_body, 200
        response_body['message'] = 'Character not found'
        response_body['results'] = {}
        return response_body, 404
    if request.method == 'DELETE':
        character = db.session.execute(db.select(Characters).where(Characters.id == character_id)).scalar()
        if character:
            db.session.delete(character)
            db.session.commit()
            response_body['message'] = 'Character deleted'
            response_body['results'] = {}
        response_body['message'] = 'Character deleted'
        response_body['results'] = {}
        return response_body, 200


#Lógica para planets

@api.route('/planets', methods=['GET', 'POST'])
def handle_planets():
    response_body={}
    if request.method == 'GET':
        planets = db.session.execute(db.select(Planets)).scalars()
        results = [row.serialize() for row in planets]
        response_body['results'] = results
        response_body['message'] = "Planets List"
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        row = Planets()
        row.name = data['name']
        row.diameter = data['diameter']
        db.session.add(row)
        db.session.commit()
        response_body['results'] = row.serialize()
        response_body['message'] = 'Character created'
        return response_body, 200


@api.route('/planets/<int:planet_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_planet(planet_id):
    response_body = {}
    if request.method == 'GET':
        planet = db.session.execute(db.select(Planets).where(Planets.id == planet_id)).scalar()
        if planet:
            response_body['results'] = planet.serialize()
            response_body['message'] = 'Planet found'
            return response_body, 200
        response_body['message'] = 'Planet not found'
        response_body['results'] = {}
        return response_body, 404
    if request.method == 'PUT':
        data = request.json
        planet = db.session.execute(db.select(Planets).where(Planets.id == planet_id)).scalar()
        if planet:
            planet.name = data['name']
            planet.description = data['description']
            planet.home_world = data['home_world']
            db.session.commit()
            response_body['message'] = 'Planet update'
            response_body['results'] = planet.serialize()
            return response_body, 200
        response_body['message'] = 'Planet not found'
        response_body['results'] = {}
        return response_body, 404
    if request.method == 'DELETE':
        planet = db.session.execute(db.select(Planets).where(Planets.id == planet_id)).scalar()
        if planet:
            db.session.delete(planet)
            db.session.commit()
            response_body['message'] = 'Planet deleted'
            response_body['results'] = {}
        response_body['message'] = 'Planet deleted'
        response_body['results'] = {}
        return response_body, 200
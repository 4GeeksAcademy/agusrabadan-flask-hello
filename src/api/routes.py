"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from api.models import db, Users, Posts, Comments

api = Blueprint('api', __name__)
CORS(api)# Allow CORS requests to this API


@api.route('/hello', methods=['GET'])
def handle_hello():
    response_body={}
    response_body ["message"] = "Hello! I'm a message that came from the backend"
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
            # db.session.delete(user)
            user.is_active = False
            db.session.commit()
            response_body['message'] = 'Usuario eliminado'
            response_body['results'] = {}
        response_body['message'] = 'Usuario inexistente'
        response_body['results'] = {}
        return response_body, 200

#Rutas para mi pestaña POSTS
@api.route('/posts', methods=['GET', 'POST'])
def handle_posts():
    response_body={}
    if request.method == 'GET':
        posts = db.session.execute(db.select(Posts)).scalars()
        results = [row.serialize() for row in posts]
        response_body['results'] = results
        response_body['message'] = "Posts List"
        return response_body, 200
    if request.method == 'POST':
        response_body['message'] = "Not valid endpoint, must LOGIN"
        return response_body, 404


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
def handle_comments():
    response_body={}
    if request.method == 'GET':
        comments = db.session.execute(db.select(Comments)).scalars()
        results = [row.serialize() for row in comments]
        response_body['results'] = results
        response_body['message'] = "Comments List"
        return response_body, 200
    if request.method == 'POST':
        response_body['message'] = "Not valid endpoint, must LOGIN"
        return response_body, 404


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
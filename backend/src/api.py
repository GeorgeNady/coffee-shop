#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Drink
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()


## -----------------------------------------------------------
## ---------------------------------------------------- ROUTES
## -----------------------------------------------------------

# DONE implementing endpoint => GET /drinks

@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    formatted_drinks = [drink.short() for drink in drinks]

    return (jsonify({'success': True, 'drinks': formatted_drinks}), 200)


# DONE implementing endpoint => GET /drinks-detail

@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        drinks = Drink.query.all()
        formatted_drinks = [drink.long() for drink in drinks]
        return (jsonify({'success': True, 'drinks': formatted_drinks}),
                200)
    except Exception:
        abort(422)


# DONE implementing endpoint => POST /drinks

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(payload):
    try:
        req = request.get_json()
        title = req.get('title', None)
        recipe = json.dumps(req.get('recipe', None))
        drink = Drink(title=title, recipe=recipe)

        drink.insert()

        return (jsonify({'success': True, 'drinks': [drink.long()]}),
                200)
    except Exception:

        abort(422)


# DONE implementing endpoint => PATCH /drinks/<id>

@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(payload, id):
    try:
        req = request.get_json()
        drink = Drink.query.filter_by(id=id).first()

        if drink is None:
            abort(404)

        if req.get('title', None) is not None:
            drink.title = req.get('title', None)

        if req.get('recipe', None) is not None:
            drink.recipe = json.dumps(req.get('recipe', None))

        drink.update()

        return jsonify({'success': True, 'drinks': [drink.long()]})
    except Exception:

        abort(422)


# DONE implementing endpoint => DELETE /drinks/<id>

@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    try:
        drink = Drink.query.filter_by(id=id).one_or_none()

        if drink is None:
            abort(404)

        drink.delete()

        return (jsonify({'success': True, 'delete': id}), 200)
    except Exception:

        abort(422)


## ----------------------------------------------------------
## ------------------------------------------- Error Handling
## ----------------------------------------------------------

# DONE implementing error handler for 422

@app.errorhandler(422)
def unprocessable(error):
    return (jsonify({'success': False, 'error': 422,
            'message': 'unprocessable'}), 422)


# DONE implementing error handler for 404

@app.errorhandler(404)
def not_found(error):
    return (jsonify({'success': False, 'status code': 404,
            'message': 'not found'}), 404)


# DONE implementing error handler for 401

@app.errorhandler(401)
def not_authorized(error):
    return (jsonify({'success': False, 'error': 401,
            'message': 'not authorized'}), 401)


# DONE implementing error handler for 500

@app.errorhandler(500)
def server_error(error):
    return (jsonify({'success': False, 'error': 500,
            'message': 'internal server error'}), 500)


# DONE implementing error handler for 400

@app.errorhandler(400)
def bad_request(error):
    return (jsonify({'success': False, 'error': 400,
            'message': 'Bad Request'}), 400)


# DONE implementing error handler for AuthError

@app.errorhandler(AuthError)
def auth_error(auth_error):
    return (jsonify({'success': False, 'error': auth_error.status_code,
            'message': auth_error.error['description']}),
            auth_error.status_code)

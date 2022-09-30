import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks')
@requires_auth(permission='get:drinks')
def view_drinks(payload):
    drinks_query = Drink.query.order_by(Drink.id).all()
    drinks = list()
    
    if not drinks_query:
        abort(404)
    else:
        for drink in drinks_query:
            print('drink', drink)
            drinks.append(drink.short())
            
        return jsonify({
            'success': True,
            'drinks': drinks
        })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks-detail')
@requires_auth(permission='get:drinks-detail')
def view_drinks_detail(payload):
    drinks_query = Drink.query.order_by(Drink.id).all()
    drinks = list()
    
    if not drinks_query:
        abort(404)
    else:
        for drink in drinks_query:
            drinks.append(drink.long())
            
        return jsonify({
            'success': True,
            'drinks': drinks
        })
        
        
'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing all drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth(permission='post:drinks')
def create_drinks(payload):
    body = request.get_json()
    if body is None:
        abort(400)
    else:
        try:
            title = body.get('title')
            recipe = body.get('recipe')
            #recipe is an array, convert to json string before storing in database
            recipe_json = json.dumps(recipe)
            print('recipe', recipe_json)
            new_drink = Drink(title = title, recipe = recipe_json)
            new_drink.insert()
            
            drinks = list()
            drinks_query = Drink.query.order_by(Drink.id).all()
            for drink in drinks_query:
                drinks.append(drink.long())
                
        except:
            abort(422)
        return jsonify({
            'success': True,
            'drinks': drinks
        })

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<drink_id>', methods=['PATCH'])
@requires_auth(permission='patch:drinks')
def edit_drinks(payload, drink_id):
    body = request.get_json()
    if body is None:
        abort(400)
    try:
        current_drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if current_drink is None:
            abort(404)
        title = body.get('title')
        recipe = body.get('recipe')
        #recipe is an array, convert to json string before storing in database
        recipe_json = json.dumps(recipe)
        
        current_drink.title = title
        current_drink.recipe = recipe_json
        current_drink.update()
    except:
        abort(422)
    return jsonify({
        'success': True,
        'drinks': current_drink.long()
    })

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<drink_id>', methods=['DELETE'])
@requires_auth(permission='delete:drinks')
def delete_drinks(payload, drink_id):
    current_drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if current_drink is None:
        abort(404)
    try:
        current_drink.delete()
    except:
        abort(422)
    return jsonify({
        'success': True,
        'id': current_drink.id
    })


# Error Handling
'''
Error handling for unprocessable entity
'''

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
    }), 401

@app.errorhandler(AuthError)
def authentication_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), 401
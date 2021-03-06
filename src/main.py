#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask, request, jsonify, url_for, make_response   
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Dish, Restaurant, Gender, Role, SeedData, FileContents, City, SearchDishSearch
from flask import request
from flask_sqlalchemy import SQLAlchemy
#login
from werkzeug.security import generate_password_hash, check_password_hash
import uuid 
import jwt
import datetime
from functools import wraps


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SECRET_KEY']='Th1s1ss3cr3t'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code
# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
# USERS
#get all users
@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    all_people = list(map(lambda x: x.serialize(), users))
    return jsonify(all_people), 200

# Modificar o traer un user (¿¿Cómo modificar pwd??)
@app.route('/user/<int:user_id>', methods=['PUT', 'GET'])
def get_single_user(user_id):
    body = request.get_json() #{ 'username': 'new_username'} 
    if request.method == 'PUT':
        user1 = User.query.get(user_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)
        if "email" in body:
            user1.email = body["email"]
        db.session.commit()
    if request.method == 'GET':
        user1 = User.query.get(user_id)
    return jsonify(user1.serialize()), 200 
#Eliminar un user
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_single_user(user_id):
    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user1)
    db.session.commit()    
    return jsonify(user1.serialize()), 200    
# DISHES
#get all dishes
@app.route('/dish', methods=['GET'])
def get_dishes():
    dishes = Dish.query.all()
    all_dishes = list(map(lambda x: x.serialize(), dishes))
    return jsonify(all_dishes), 200
#create dish
@app.route('/dish', methods=['POST'])
def create_users():
    request_dish = request.get_json()
    dish1 = Dish(
        name=request_dish["name"], 
        description=request_dish["description"], 
        is_typical=request_dish["is_typical"], 
        restaurant_id=request_dish["restaurant_id"]) 
    db.session.add(dish1)
    db.session.commit()
    return jsonify(dish1.serialize()), 200
#probando a cargar archivos
@app.route('/upload', methods=['GET','PUT'])
def upload():
    if request.method=="PUT":
        file = request.files["fileinput"]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename ))
        return redirect(request.url)

# Modificar o traer un dish
@app.route('/dish/<int:dish_id>', methods=['PUT', 'GET'])
def get_single_dish(dish_id):
    body = request.get_json()
    if request.method == 'PUT':
        dish1 = Dish.query.get(dish_id)
        if dish1 is None:
            raise APIException('Dish not found', status_code=404)
        if "name" in body:
            dish.name = body["name"]
        if "description" in body:
            dish.description = body["description"]
        db.session.commit()
    if request.method == 'GET':
        dish1 = Dish.query.get(dish_id)
    return jsonify(dish1.serialize()), 200 
#Eliminar un dish
@app.route('/dish/<int:dish_id>', methods=['DELETE'])
def delete_single_dish(dish_id):
    dish1 = Dish.query.get(dish_id)
    if dish1 is None:
        raise APIException('Dish not found', status_code=404)
    db.session.delete(dish1)
    db.session.commit()    
    return jsonify(dish1.serialize()), 200  
# RESTAURANT
# get all restaurant
@app.route('/restaurant', methods=['GET'])
def get_restaurant():
    restaurant = Restaurant.query.all()
    all_restaurants = list(map(lambda x: x.serialize(), restaurant))
    return jsonify(all_restaurants), 200

# create restaurant
@app.route('/restaurant', methods=['POST'])
def create_restaurant():
    request_restaurant = request.get_json()
    restaurant1 = Restaurant(
    name=request_restaurant["name"],
    address=request_restaurant["address"],    
    phone=request_restaurant["phone"], 
    email=request_restaurant["email"], 
    web_page=request_restaurant["web_page"],  
    is_active=request_restaurant["is_active"], 
    latitude=request_restaurant["latitude"],
    longitude=request_restaurant["longitude"],
    city_id=request_restaurant["city_id"]  ) 
    db.session.add(restaurant1)
    db.session.commit()
    return jsonify(restaurant1.serialize()), 200
# Modificar o traer un restaurant
@app.route('/restaurant/<int:restaurant_id>', methods=['PUT', 'GET'])
def get_single_restaurant(restaurant_id):
    body = request.get_json() 
    if request.method == 'PUT':
        restaurant1 = Restaurant.query.get(restaurant_id)
        if restaurant1 is None:
            raise APIException('Restaurant not found', status_code=404)
        if "name" in body:
            restaurant1.name = body["name"]
        if "email" in body:
            restaurant1.email = body["email"]
        if "address" in body:
            restaurant1.address = body["address"]
        if "phone" in body:
            restaurant1.phone = body["phone"]
        if "web_page" in body:
            restaurant1.web_page = body["web_page"]
        db.session.commit()
    if request.method == 'GET':
        restaurant1 = Restaurant.query.get(restaurant_id)
    return jsonify(restaurant1.serialize()), 200 
#Eliminar un restaurant
@app.route('/restaurant/<int:restaurant_id>', methods=['DELETE'])
def delete_single_restaurant(restaurant_id):
    restaurant1 = User.query.get(restaurant_id)
    if restaurant1 is None:
        raise APIException('Restaurant not found', status_code=404)
    db.session.delete(restaurant1)
    db.session.commit()    
    return jsonify(restaurant1.serialize()), 200   

# get all cities
@app.route('/city', methods=['GET'])
def get_cities():
    cities = City.query.all()
    all_cities = list(map(lambda x: x.serialize(), cities))
    return jsonify(all_cities), 200
# create city
@app.route('/city', methods=['GET'])
def create_city():
    request_city = request.get_json()
    city1 = City(
    name=request_city["name"],
    )
    db.session.add(city1)
    db.session.commit()
    return jsonify(city1.serialize()), 200
# Modificar o traer una city
@app.route('/city/<int:city_id>', methods=['PUT', 'GET'])
def get_single_city(city_id):
    body = request.get_json()
    if request.method == 'PUT':
        city1 = City.query.get(city_id)
        if city1 is None:
            raise APIException('Dish not found', status_code=404)
        if "name" in body:
            city.name = body["name"]
        db.session.commit()
    if request.method == 'GET':
        city1 = City.query.get(city_id)
    return jsonify(city1.serialize()), 200 
@app.route('/search', methods=['GET', 'POST'])
def search_results():
    args2=request.args.to_dict(flat=False)
    lugar =''
    plato =''
    if args2['lugar'] != ['']:
        lugar = args2['lugar'][0].lower()
    else:
       return jsonify({'msg':'Es necesario rellenar este campo, amigo!'}), 301
        
    if args2['plato'] != ['undefined']:
        plato = args2['plato'][0].lower()
    else:
        plato = args2['plato']
   
    return "Not query string", 200  
@app.route('/render_results', methods=['GET'])
def render_results():
    args2=request.args.to_dict(flat=False)
    if not('lugar'in args2) and not('plato'in args2): 
      raise APIException('Info not found', status_code=400)
    elif not('lugar'in args2):
      raise APIException('Dish not found', status_code=400)
    else:
      city = args2['lugar'][0].lower() if 'lugar' in args2 else None
      dish = args2['plato'][0].lower() if 'plato' in args2 and len(args2['plato'][0])>0 else None 
      seeker = SearchDishSearch()
      dishes = seeker.search(city, dish)
    return jsonify({"info": dishes}), 200  
@app.route('/restaurantInfo/<int:rest_id>', methods=['GET'])
def restInfo(rest_id):
    body = rest_id
    print(body)
    rest = Restaurant.query.get(rest_id)
    print(rest)
    return jsonify(rest.serialize()), 200   
def token_required(f):  
    @wraps(f)  
    def decorator(*args, **kwargs):
        token = None 
        if 'x-access-tokens' in request.headers:  
            token = request.headers['x-access-tokens'] 
        if not token:  
            return jsonify({'message': 'a valid token is missing'})   
        try:  
            data = jwt.decode(token, app.config["SECRET_KEY"]) 
            current_user = Users.query.filter_by(id=data['id']).first()  
        except:  
            return jsonify({'message': 'token is invalid'})
        return f(current_user, *args, **kwargs)
    return decorator 
@app.route('/register', methods=['GET', 'POST'])
def signup_user():  
 data = request.get_json()  
 print(data)
 new_user = User(email=data['email'], password=data['password']) 
 print(new_user)
 db.session.add(new_user)  
 db.session.commit()    
 return jsonify({'message': 'registered successfully'})  
 
@app.route('/login', methods=['GET', 'POST'])  
def login_user(): 
    auth = request.authorization  
    print(auth)
    if not auth or not auth["username"] or not auth["password"]:  
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    
    user = User.query.filter_by(email=auth["username"]).first()   
    print(user.password, auth["password"])
    if user.password == auth["password"]:
        token = jwt.encode({'id': user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY']) 
        print("4",token) 
        return jsonify({'token' : token.decode('UTF-8')}) 
    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})
from tokenize import Token
from flask import Flask, jsonify, request, Response
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import hashlib
from functools import wraps
from bson import ObjectId
import datetime
import json
import jwt
import pymongo
import os

app = Flask(__name__)
api = Api(app)


user_details = reqparse.RequestParser()
user_details.add_argument("first_name", type=str, help="Input first name of user", required=True)
user_details.add_argument("last_name", type=str, help="Input last name of user", required=True)
user_details.add_argument("email", type=str, help="Input user email", required=True)
user_details.add_argument("password", type=str, help="Input user password", required=True)

login_details = reqparse.RequestParser()
login_details.add_argument("email", type=str, help="Input user email", required=True)
login_details.add_argument("password", type=str, help="Input user password", required=True)

template_details = reqparse.RequestParser()
template_details.add_argument("template_name", type=str, help="Input template name", required=True)
template_details.add_argument("subject", type=str, help="Input template subject", required=True)
template_details.add_argument("body", type=str, help="Input template body", required=True)

template_put_details = reqparse.RequestParser()
template_put_details.add_argument("template_name", type=str, help="Input template name")
template_put_details.add_argument("subject", type=str, help="Input template subject")
template_put_details.add_argument("body", type=str, help="Input template body")

# Resource Fields
resource_fields = {
    '_id':fields.String,
    'template_name': fields.String,
    'subject': fields.String,
    'body': fields.String

}

login_fields = {
    '_id':fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'token': fields.String

}

# initi mongodb
try:
    mongo = pymongo.MongoClient(f"{os.getenv('MongoClient')}", 25000)
    db = mongo.templatedb
    print("#" * 30)
    print("Database connected")
    print("#" * 30)
except Exception as e:
    print("#" * 30)
    print("Database connection Error")
    print(e)
    print("#" * 30)


# JWT Token
def check_for_token(func):
    
    @wraps(func)
    def wrapped(*args, **kwargs):
        auth = request.headers.get('authorization')
        if not auth:
            return Response(json.dumps({'message': 'no token'}), status = 400)
        
        token = auth.split(' ')[1]
        try:
            data = jwt.decode(token, b'SECRET_KEY', algorithms=['HS256'])
            setattr(request, 'data', data)
        except:
            return Response(json.dumps({'message': 'Invalid token'}), status = 403)
        return func(*args, **kwargs)
    return wrapped
    

def create_token(id):
    token = jwt.encode({ 'id' : id, 'exp': datetime.datetime.now() + datetime.timedelta(seconds=60*60*24*30)}, b'SECRET_KEY', algorithm='HS256')
    
    return token


# Harsh Password
def harsh_password(text):
    return hashlib.pbkdf2_hmac('sha256', text.encode(), b'SECRET', 100000).hex()



# Check For Errors
def abort_wrong_email(text):
    if '@' not in text:
        abort(400, message="Email is not valid")

def abort_wrong_login(args):
    if not db.user.find_one({'email': args.email}) or db.user.find_one({'email':args.email})['password'] != args.password:
        abort(400, message="Invalid email or password")

def abort_user_exist(text):
    if db.user.find_one({'email': text}):
        abort(400, message="User already exist")


def abort_template_doesnt_exist(temp_id, user_id):
    if not db.templates.find_one({ '_id': ObjectId(temp_id),'id': user_id}):
        abort(404, message="Template doesn't exist for user")

def drop_none(args):
    valid = {}
    for key, val in args.items():
        if val is not None:
            valid[key] = val
    return valid



class register(Resource):

    def post(self):
        args = user_details.parse_args()
        abort_wrong_email(args.email)
        abort_user_exist(args.email)
        args.password = harsh_password(args.password)
        db.user.insert_one(args)
        return Response(status=201)
        
class login(Resource):

    @marshal_with(login_fields)
    def post(self):
        args = login_details.parse_args()
        abort_wrong_email(args.email)
        args.password = harsh_password(args.password)
        abort_wrong_login(args)
        curr_user = db.user.find_one({'email':args.email}, {'password':0})
        token= create_token(f'{curr_user["_id"]}')
        curr_user['token'] = token
        return curr_user


class template(Resource):
    
    @check_for_token
    @marshal_with(resource_fields)
    def get(self):
        id = request.data['id']
        return [doc for doc in db.templates.find({'id':id})]

    @check_for_token
    def post(self):
        args = template_details.parse_args()
        args['id'] = request.data['id']
        db.templates.insert_one(args)
        return Response(status=201)



class template_1(Resource):
    @check_for_token
    @marshal_with(resource_fields)
    def get(self, temp_id):
        abort_template_doesnt_exist(temp_id, request.data['id'])
        return db.templates.find_one({'_id': ObjectId(temp_id)})
    
    @check_for_token
    def put(self, temp_id):
        args = template_put_details.parse_args()
        abort_template_doesnt_exist(temp_id, request.data['id'])
        args = drop_none(args)
        db.templates.update_one({'_id':ObjectId(temp_id)}, {"$set": args})
        return Response(status=200)

    @check_for_token
    def delete(self, temp_id):
        abort_template_doesnt_exist(temp_id, request.data['id'])
        db.templates.delete_one({'_id': ObjectId(temp_id)})
        return Response(status=204)



# URLS

api.add_resource(register, '/register')
api.add_resource(login, '/login')
api.add_resource(template,'/template')
api.add_resource(template_1,'/template/<string:temp_id>')



if __name__ == '__main__':
    app.run(debug = True)
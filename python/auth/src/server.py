import jwt, os
from flask import Flask, request
from flask_pymongo import PyMongo
from pymongo.collection import ReturnDocument
from bson import ObjectId
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import constants

load_dotenv()

server = Flask(__name__)

db_user_name = os.environ.get("MONGODB_USERNAME")
db_user_pwd = os.environ.get("MONGODB_PWD")
db_host = os.environ.get("MONGODB_HOST")
db_port = os.environ.get("MONGODB_PORT")
db_name = os.environ.get("MONGODB_DB")
mongo_uri = f"{db_user_name}:{db_user_pwd}@{db_host}:{db_port}/{db_name}"

server.config["MONGO_URI"] = f"mongodb://{mongo_uri}"
mongo = PyMongo(server)

@server.route("/sign-up", methods=["POST"])
def signUp():
    email = request.get_json()['email']
    password = request.get_json()['password']
    code_activation = request.get_json()['code_activation']
   
    try:      
        user = mongo.db.user.find_one({
            "email":email
        })
        
        if user:
            return constants.EMAIL_ALREADY_EXISTS, constants.HTTP_STATUS_BAD_REQUEST
        else:
            user = { 
                "email" : email, 
                "password" : password,
                "codeActivation" : code_activation,
                "activated": False 
            }
            
            mongo.db.user.insert_one(user)
            
            return constants.USER_INSERTED, constants.HTTP_STATUS_CREATE
    except Exception as e:
        return e, constants.HTTP_STATUS_INTERNAL_SERVER_ERROR
    
@server.route("/activate-account", methods=["PUT"])
def activateAccount():
    email = request.get_json()['email']
    code_activation = request.get_json()['code_activation']
    
    try:
        updated_document = mongo.db.user.find_one_and_update(
        {
            "email": email,
            "codeActivation": code_activation,
            "activated" : False
        },
        {
            "$set": 
                {
                    "activated": True
                }
            },
        return_document=ReturnDocument.AFTER)
        return updated_document
    except Exception as e:
        return e, constants.HTTP_STATUS_INTERNAL_SERVER_ERROR
    

@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization

    if not auth:
        return constants.MISSING_CREDENTIALS, constants.HTTP_STATUS_UNAUTHORIZED
    
    try:      
        user = mongo.db.user.find_one({
            "email": auth.username
        })
        
        if user:
            activated = user["activated"]
            
            if activated == False:
                return constants.USER_NOT_ACTIVE, constants.HTTP_STATUS_BAD_REQUEST
            else: 
                email = user["email"]
                password = user["password"]
                
                if auth.username != email or auth.password != password:
                    return constants.INVALID_CREDENTIALS, constants.HTTP_STATUS_UNAUTHORIZED
                else:
                    return createJWT(email, os.environ.get("JWT_SECRET"), True)
        else:
            return constants.INVALID_CREDENTIALS, constants.HTTP_STATUS_UNAUTHORIZED
    except Exception as e:
        return e, constants.HTTP_STATUS_INTERNAL_SERVER_ERROR

@server.route("/event", methods=["POST"])
def addEvent():
    
    try:
        # substituir pelo token
        username = "festrela@email.com"  
        user = mongo.db.user.find_one({
            "email": username
        })
           
        if user:
            description = request.get_json()['description']
            mongo.db.event.insert_one({
                "description": description,
                "user": user["_id"]
            })
            
            return constants.EVENT_INSERTED, constants.HTTP_STATUS_CREATE
            
    except Exception as e:
        return e, constants.HTTP_STATUS_INTERNAL_SERVER_ERROR
    
@server.route("/event", methods=["GET"])
def getEvents():
    
    try:
        events = []
        for doc in mongo.db.event.find({}):
            events.append(doc)
                  
        return events
            
    except Exception as e:
        return e, constants.HTTP_STATUS_INTERNAL_SERVER_ERROR
    
@server.route("/event", methods=["DELETE"])
def deleteEvent():
    
    try:
        id = request.get_json()['id']
        mongo.db.event.find_one_and_delete(
            {
                "_id":  ObjectId(id)
            }
        )        
                  
        return constants.EVENT_DELETED, constants.HTTP_STATUS_OK
            
    except Exception as e:
        return e, constants.HTTP_STATUS_INTERNAL_SERVER_ERROR
    
@server.route("/validate-token", methods=["POST"])
def validateToken():
    encoded_jwt = request.headers["Authorization"]
    
    if not encoded_jwt:
        return constants.MISSING_CREDENTIALS, constants.HTTP_STATUS_UNAUTHORIZED
    
    encoded_jwt = encoded_jwt.split(" ")[1]
    
    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )
    except:
        return constants.NOT_AUTHORIZED, constants.HTTP_STATUS_FORBIDDEN
    
    return decoded, constants.HTTP_STATUS_OK
 
def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.now(timezone.utc) + timedelta(days=1),
            "iat": datetime.now(timezone.utc),
            "admin": authz
        },
        secret,
        algorithm="HS256"   
    )
    
port = os.environ.get("SERVER_AUTH_PORT")
if __name__ == "__main__":
    server.run(debug=True, host="0.0.0.0", port=port)
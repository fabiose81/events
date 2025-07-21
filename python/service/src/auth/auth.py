import jwt, os
from flask import request
from pymongo.collection import ReturnDocument
from datetime import datetime, timezone, timedelta
import constants

import email_sender

def signUp(mongo):
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    code_activation = request.get_json()["code_activation"]
       
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
            
        with mongo.cx.start_session() as session:
            with session.start_transaction():
                try:
                    mongo.db.user.insert_one(user, session=session)
                    result, err = email_sender.send(email, code_activation) 
                    if err: 
                       session.abort_transaction() 
                       return constants.USER_EXCEPTION, constants.HTTP_STATUS_BAD_REQUEST
                   
                    return constants.USER_INSERTED, constants.HTTP_STATUS_CREATE 
                except Exception as e:
                    return e, constants.HTTP_STATUS_INTERNAL_SERVER_ERROR
                
def activateAccount(mongo):
    email = request.get_json()["email"]
    code_activation = request.get_json()["code_activation"]
    
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
        
        if (not updated_document):
            return constants.ACCOUNT_ALREADY_ACTIVATED
        else:
            return constants.ACCOUNT_ACTIVATED
    except Exception as e:
        return e, constants.HTTP_STATUS_INTERNAL_SERVER_ERROR
    
def login(mongo):
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
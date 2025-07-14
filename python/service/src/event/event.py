from flask import request
from bson import ObjectId
import constants

def addEvent(mongo):
    try:
        username =  request.get_json()["username"]
        user = mongo.db.user.find_one({
            "email": username
        })
           
        if user:
            description = request.get_json()["description"]
            mongo.db.event.insert_one({
                "description": description,
                "user": user["_id"]
            })
            
            return constants.EVENT_INSERTED, constants.HTTP_STATUS_CREATE
            
    except Exception as e:
        return e, constants.HTTP_STATUS_INTERNAL_SERVER_ERROR
    
def getEvents(mongo, username):
    try:
        user = mongo.db.user.find_one({
            "email": username
        })
        events = []
        if user:         
            for doc in mongo.db.event.find({"user": user["_id"]}):
                events.append(doc)
                  
        return events
            
    except Exception as e:
        return e, constants.HTTP_STATUS_INTERNAL_SERVER_ERROR
    
def deleteEvent(mongo):   
    try:
        id = request.get_json()["id"]
        mongo.db.event.find_one_and_delete(
            {
                "_id":  ObjectId(id)
            }
        )        
                  
        return constants.EVENT_DELETED, constants.HTTP_STATUS_OK
            
    except Exception as e:
        return e, constants.HTTP_STATUS_INTERNAL_SERVER_ERROR
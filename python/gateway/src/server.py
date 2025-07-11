import os
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS 

import access
import account
import event

load_dotenv()

server = Flask(__name__)
CORS(server)

@server.route("/health", methods=["GET"])
def health():
    return "OK", 200

@server.route("/sign-up", methods=["POST"])
def signUp(): 
    response, err = account.signUp(request)

    if not err:
        return response
    else:
        return err
    
@server.route("/login", methods=["POST"])
def login():     
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err
    
@server.route("/active", methods=["GET"])
def active(): 
    response, err = account.activateAccount(request)
    
    if not err:
        return response
    else:
        return err
    
@server.route("/event", methods=["POST"])
def addEvent():  
    token, errToken = access.token(request) 
    if not errToken:   
        response, errEvent = event.addEvent(request)

        if not errEvent:
            return response
        else:
            return errEvent
    else:
        return errToken[0], errToken[1]     
    
@server.route("/event", methods=["GET"])
def getEvents():     
    token, errToken = access.token(request)       
    if not errToken:   
        response, errEvent = event.getEvents()

        if not errEvent:
            return response
        else:
            return errEvent
    else:
        return errToken[0], errToken[1]    
    
@server.route("/event", methods=["DELETE"])
def deleteEvent():   
    token, errToken = access.token(request) 
    if not errToken:   
        response, errEvent = event.deleteEvent(request)

        if not errEvent:
            return response
        else:
            return errEvent
    else:
        return errToken[0], errToken[1]
    
port = os.environ.get("SERVER_GATEWAY_PORT")
if __name__ == "__main__":
    server.run(debug=True, host="0.0.0.0", port=port)
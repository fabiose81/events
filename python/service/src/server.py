import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), './auth/'))
sys.path.append(os.path.join(os.path.dirname(__file__), './event/'))

from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import auth
import event

load_dotenv()

server = Flask(__name__)

db_user_name = os.environ.get("MONGODB_USERNAME")
db_user_pwd = os.environ.get("MONGODB_PWD")
db_hosts_ports = os.environ.get("MONGODB_HOSTS_PORTS")
db_name = os.environ.get("MONGODB_DB")
db_replica_set = os.environ.get("MONGODB_REPLICA_SET")

mongo_uri = f"{db_user_name}:{db_user_pwd}@{db_hosts_ports}/{db_name}?{db_replica_set}"
server.config["MONGO_URI"] = f"mongodb://{mongo_uri}"
mongo = PyMongo(server)

try:
    mongo.cx.admin.command("ping")
    print("✅ Connected to MongoDB")
except Exception as e:
      print("❌ MongoDB authentication failed:", e)
    
@server.route("/sign-up", methods=["POST"])
def signUp():
    return auth.signUp(mongo)
    
@server.route("/activate-account", methods=["PUT"])
def activateAccount():
    return auth.activateAccount(mongo)  

@server.route("/login", methods=["POST"])
def login():
    return auth.login(mongo)

@server.route("/event", methods=["POST"])
def addEvent():
    return event.addEvent(mongo)
    
@server.route("/event/<username>", methods=["GET"])
def getEvents(username):
    return event.getEvents(mongo, username)
    
@server.route("/event", methods=["DELETE"])
def deleteEvent():
    return event.deleteEvent(mongo)
    
@server.route("/validate-token", methods=["POST"])
def validateToken():
    return auth.validateToken()
     
port = os.environ.get("SERVER_AUTH_PORT")
if __name__ == "__main__":
    server.run(debug=True, host="0.0.0.0", port=port)
import os, requests
import constants

def addEvent(request, username):
    description = request.get_json()["description"]
    
    event = {
        "description" : description,
        "username" : username
    }
    
    response = requests.post(
        f"http://{os.environ.get("SVC_ADDRESS")}/event", json=event
    )
    
    if response.status_code == constants.HTTP_STATUS_OK:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
    
def getEvents(username):
    
    response = requests.get(
        f"http://{os.environ.get("SVC_ADDRESS")}/event/{username}"
    )
    
    if response.status_code == constants.HTTP_STATUS_OK:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
    
def deleteEvent(request):
    id = request.get_json()["id"]
    
    event = {
        "id": id
    }

    response = requests.delete(
        f"http://{os.environ.get("SVC_ADDRESS")}/event", json=event
    )
    
    if response.status_code == constants.HTTP_STATUS_OK:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
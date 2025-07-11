import os, requests
import constants

def addEvent(request):
    description = request.get_json()["description"]
    
    event = {
        "description": description
    }
    
    response = requests.post(
        f"http://{os.environ.get("AUTH_SVC_ADDRESS")}/event", json=event
    )
    
    if response.status_code == constants.HTTP_STATUS_OK:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
    
def getEvents():
    
    response = requests.get(
        f"http://{os.environ.get("AUTH_SVC_ADDRESS")}/event"
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
        f"http://{os.environ.get("AUTH_SVC_ADDRESS")}/event", json=event
    )
    
    if response.status_code == constants.HTTP_STATUS_OK:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
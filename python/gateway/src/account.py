import os, requests
import uuid
import constants
import email_sender

def signUp(request):
    email = request.get_json()["email"]
    password = request.get_json()['password']
    code_activation = str(uuid.uuid4())
    
    user = {
            "email": email,
            "password": password,
            "code_activation": code_activation
    }

    response = requests.post(
        f"http://{os.environ.get("AUTH_SVC_ADDRESS")}/sign-up", json=user
    )
    
    if response.status_code == constants.HTTP_STATUS_OK:
        email_response, err = email_sender.send(email, code_activation)
        
        if not err:
            return response.text, None
        else:
            return None, (email_response, 400)
    else:
        return None, (response.text, response.status_code)
    
def activateAccount(request):
    email = request.args.get("email")
    code_activation = request.args.get("code")
    
    user = {
            "email": email,
            "code_activation": code_activation
    }

    response = requests.put(
        f"http://{os.environ.get("AUTH_SVC_ADDRESS")}/activate-account", json=user
    )
    
    if response.status_code == constants.HTTP_STATUS_OK:
        return constants.ACCOUNT_ACTIVATED, None
    else:
        return None, (response.text, response.status_code)
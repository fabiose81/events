import os, requests
import constants

def login(request):
    auth = request.authorization
    if not auth:
        return None, (constants.MISSING_CREDENTIALS, constants.HTTP_STATUS_UNAUTHORIZED)

    basicAuth = (auth.username, auth.password)
    
    response = requests.post(
        f"http://{os.environ.get("SVC_ADDRESS")}/login", auth=basicAuth
    )
    
    if response.status_code == constants.HTTP_STATUS_OK:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
    
def token(request):
    if not constants.AUTHORIZATION in request.headers:
        return None, (constants.MISSING_CREDENTIALS, constants.HTTP_STATUS_UNAUTHORIZED)

    token = request.headers[constants.AUTHORIZATION]

    if not token:
        return None, (constants.MISSING_CREDENTIALS, constants.HTTP_STATUS_UNAUTHORIZED)

    response = requests.post(
        f"http://{os.environ.get("SVC_ADDRESS")}/validate-token",
        headers = {
                constants.AUTHORIZATION: token
            }
    )

    if response.status_code == constants.HTTP_STATUS_OK:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
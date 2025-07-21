import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

import pytest
from unittest.mock import MagicMock, patch

from pymongo.collection import ReturnDocument

from flask import Flask

import jwt

import constants 
import auth

USERNAME = 'user@email.com'
PASSWORD = 'userPWD'
JWT_SECRET = 'jwt_secret'
CODE_ACTIVATION = '687e540a5c694a229f935fe3'

@pytest.fixture
def client():
    app = Flask(__name__)
    with app.test_request_context():
        yield app.test_client()

def test_missing_credentials(client):
    with patch('auth.request') as mock_request:
        mock_request.authorization = None
        
        mongo = MagicMock()
        response, status = auth.login(mongo)

        assert response == constants.MISSING_CREDENTIALS
        assert status == constants.HTTP_STATUS_UNAUTHORIZED
        
def test_login_user_not_found(client):
    with patch('auth.request') as mock_request:
        mock_request.authorization = MagicMock(username=USERNAME, password=PASSWORD)

        mongo = MagicMock()
        mongo.db.user.find_one.return_value = None

        response, status = auth.login(mongo)

        assert response == constants.INVALID_CREDENTIALS
        assert status == constants.HTTP_STATUS_UNAUTHORIZED
        
def test_login_user_not_activated(client):
    with patch('auth.request') as mock_request:
        mock_request.authorization = MagicMock(username=USERNAME, password=PASSWORD)

        mongo = MagicMock()
        mongo.db.user.find_one.return_value = {
            "email": USERNAME,
            "password": PASSWORD,
            "activated": False
        }

        response, status = auth.login(mongo)

        assert response == constants.USER_NOT_ACTIVE
        assert status == constants.HTTP_STATUS_BAD_REQUEST

def test_login_success(client):
    with patch('auth.request') as mock_request, \
         patch('auth.createJWT') as mock_create_jwt, \
         patch('auth.os.environ.get', return_value=JWT_SECRET):
        
        mock_request.authorization = MagicMock(username=USERNAME, password=PASSWORD)
        mock_create_jwt.return_value = 'jwt_token'

        mongo = MagicMock()
        mongo.db.user.find_one.return_value = {
            "email": USERNAME,
            "password": PASSWORD,
            "activated": True
        }

        response = auth.login(mongo)

        mock_create_jwt.assert_called_once_with(USERNAME, JWT_SECRET, True)
        assert response == 'jwt_token'
        
def test_activate_account_success(client):
    with patch('auth.request') as mock_request:
        mock_request.get_json = MagicMock(return_value={
            "email": USERNAME,
            "code_activation": CODE_ACTIVATION
        })
        
        mongo = MagicMock()
        user_updated = {
            "email": USERNAME,
            "codeActivation": CODE_ACTIVATION,
            "activated": True
        }
        
        mongo.db.user.find_one_and_update.return_value = user_updated
        
        result = auth.activateAccount(mongo)

        mongo.db.user.find_one_and_update.assert_called_once_with(
            {
                "email": USERNAME,
                "codeActivation": CODE_ACTIVATION,
                "activated": False
            },
            {
                "$set": {
                    "activated": True
                }
            },
            return_document=ReturnDocument.AFTER
        )

        assert result == constants.ACCOUNT_ACTIVATED
               
def test_validate_token_success(client):   
    token = jwt.encode({'email': USERNAME}, JWT_SECRET, algorithm='HS256')
    headers = {'Authorization': f'Bearer {token}'}
    with patch('auth.request') as mock_request, \
         patch('auth.os.environ.get', return_value=JWT_SECRET): 

         mock_request.headers = headers
    
         response, status = auth.validateToken()

         assert status == constants.HTTP_STATUS_OK
         assert response['email'] == USERNAME
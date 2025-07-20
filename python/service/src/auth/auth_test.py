import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

import pytest
from unittest.mock import MagicMock, patch

from flask import Flask, request

import constants 
import auth

@pytest.fixture
def client():
    app = Flask(__name__)
    with app.test_request_context():
        yield app.test_client()

def test_missing_credentials(client):
    with patch('auth.request') as mock_request:
        
        mongo = MagicMock()
        response, status = auth.login(mongo)

        assert response == constants.MISSING_CREDENTIALS
        assert status == constants.HTTP_STATUS_UNAUTHORIZED
        
def test_login_user_not_found(client):
    with patch('auth.request') as mock_request:
        mock_request.authorization = MagicMock(username="user@example.com", password="pass123")

        mongo = MagicMock()
        mongo.db.user.find_one.return_value = None

        response, status = auth.login(mongo)

        assert response == constants.INVALID_CREDENTIALS
        assert status == constants.HTTP_STATUS_UNAUTHORIZED
        
def test_login_user_not_activated(client):
    with patch('auth.request') as mock_request:
        mock_request.authorization = MagicMock(username="user@example.com", password="pass123")

        mongo = MagicMock()
        mongo.db.user.find_one.return_value = {
            "email": "user@example.com",
            "password": "pass123",
            "activated": False
        }

        response, status = auth.login(mongo)

        assert response == constants.USER_NOT_ACTIVE
        assert status == constants.HTTP_STATUS_BAD_REQUEST

def test_login_success(client):
    with patch('auth.request') as mock_request, \
         patch('auth.createJWT') as mock_create_jwt, \
         patch('auth.os.environ.get', return_value='secret'):
        
        mock_request.authorization = MagicMock(username="user@example.com", password="pass123")
        mock_create_jwt.return_value = 'jwt_token'

        mongo = MagicMock()
        mongo.db.user.find_one.return_value = {
            "email": "user@example.com",
            "password": "pass123",
            "activated": True
        }

        response = auth.login(mongo)

        mock_create_jwt.assert_called_once_with("user@example.com", 'secret', True)
        assert response == 'jwt_token'
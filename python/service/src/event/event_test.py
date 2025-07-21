import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from bson import ObjectId

import pytest
from unittest.mock import MagicMock, patch

from flask import Flask

import constants 
import event

USERNAME = 'user@email.com'
EVENT_DESCRIPTION = 'Go to gym'
EVENT_DESCRIPTION_2 = 'Clear home'

@pytest.fixture
def client():
    app = Flask(__name__)
    with app.test_request_context():
        yield app.test_client()

def test_get_events_success():
    user_id = ObjectId("64cfe82420aee5a5d205c1b7")
    mock_user = {"_id": user_id, "email": USERNAME}
    mock_events = [
        {"_id": ObjectId(), "description": EVENT_DESCRIPTION, "user": user_id},
        {"_id": ObjectId(), "description": EVENT_DESCRIPTION_2, "user": user_id}
    ]
    
    mongo = MagicMock()
    mongo.db.user.find_one.return_value = mock_user
    mongo.db.event.find.return_value = mock_events
    
    result = event.getEvents(mongo, USERNAME)
    
    mongo.db.user.find_one.assert_called_once_with({"email": USERNAME})
    mongo.db.event.find.assert_called_once_with({"user": user_id})
    
    assert result == mock_events
    
     
def test_add_event(client):
    with patch('event.request') as mock_request:
        mock_request.get_json = MagicMock(return_value={
            "username": USERNAME,
            "description": EVENT_DESCRIPTION
        })
       
        mongo = MagicMock()
        mock_user = {"_id": "user_id"}
        mongo.db.user.find_one.return_value = mock_user
        
        mongo.db.event.insert_one({
            "description": EVENT_DESCRIPTION,
            "user": "687c5a03e08ff16febff0da8"
        })
        
        response, status = event.addEvent(mongo)

        assert response == constants.EVENT_INSERTED
        assert status == constants.HTTP_STATUS_CREATE
        
def test_delete_event(client):
    with patch('event.request') as mock_request:
        mock_request.get_json = MagicMock(return_value={
            "id": "687c5a03e08ff16febff0da9"
        })
       
        mongo = MagicMock()

        response, status = event.deleteEvent(mongo)
        
        mongo.db.event.find_one_and_delete.assert_called_once_with({
            "_id": ObjectId("687c5a03e08ff16febff0da9")
        })

        assert response == constants.EVENT_DELETED
        assert status == constants.HTTP_STATUS_OK
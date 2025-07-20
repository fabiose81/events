import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from bson import ObjectId

import pytest
from unittest.mock import MagicMock, patch

from flask import Flask, request

import constants 
import event

@pytest.fixture
def client():
    app = Flask(__name__)
    with app.test_request_context():
        yield app.test_client()

def test_get_events_success():
    user_id = ObjectId("64cfe82420aee5a5d205c1b7")
    mock_user = {"_id": user_id, "email": "user@example.com"}
    mock_events = [
        {"_id": ObjectId(), "description": "Go to gum", "user": user_id},
        {"_id": ObjectId(), "description": "Clear home", "user": user_id}
    ]
    
    mongo = MagicMock()
    mongo.db.user.find_one.return_value = mock_user
    mongo.db.event.find.return_value = mock_events
    
    result = event.getEvents(mongo, "user@example.com")
    
    mongo.db.user.find_one.assert_called_once_with({"email": "user@example.com"})
    mongo.db.event.find.assert_called_once_with({"user": user_id})
    
    assert result == mock_events
    
     
def test_add_event(client):
    with patch('event.request') as mock_request:
        mock_request.get_json = MagicMock(return_value={
            "username": "user@example.com",
            "description": "Go to gym"
        })
       
        mongo = MagicMock()
        mock_user = {"_id": "user_id"}
        mongo.db.user.find_one.return_value = mock_user
        
        mongo.db.event.insert_one({
            "description": "Go to gym",
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
import json
import pytest
from flask_server import app

with open('mro_response.json') as data_file:    
    data = json.load(data_file)

@pytest.fixture
def client(request):
    test_client = app.test_client()
    return test_client

def post_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url """
    return client.post(url, data=json.dumps(json_dict), content_type='application/json')

def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))

def test_login(client):
    response = post_json(client, '/login', {"password": "password", "user": 2})    
    assert response.status_code == 200     
    assert json_of_response(response) == data["login"]


def test_get_user(client):
    response = client.get('/users/2', headers={"USER":2,"PASSWORD":"password"},content_type='application/json')  
    assert response.status_code == 200     
    assert json_of_response(response) == data["get_user"]

def test_get_users_list(client):
    response = client.get('/users', headers={"USER":2,"PASSWORD":"password"},content_type='application/json')  
    assert response.status_code == 200     
    assert json_of_response(response) == data["get_user"]

def test_create_user(client):
    response = post_json(client, '/create_user', { "age": 12,"password": "password", "name": "rajkumar"})    
    assert response.status_code == 200     
    assert json_of_response(response) == data["create_user"]

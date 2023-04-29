from random import randint

from adapters import orm
from domain.commands import *
from services import message_bus

# create a test database
orm.database_url = "sqlite:///test.db"

def test_list_aircraft(client):
    response = client.get('/api/aircraft')
    assert response.status_code == 200

def test_create_aircraft(client):
    data = {
        'name': 'Test Aircraft',
        'make': 'Test Make',
        'model': 'Test Model',
        'tail_number': 'TEST123'
    }
    response = client.post('/api/aircraft', json=data)
    assert response.status_code == 200

def test_get_aircraft(client):
    response = client.get('/api/aircraft/1')
    assert response.status_code == 200
    assert response.json['tail_number'] == 'TEST123'

def test_update_aircraft(client):

    data = {
        'tail_number': 'TEST1234'
    }
    response = client.put('/api/aircraft/1', json=data)
    assert response.status_code == 200

def test_delete_aircraft(client):
    data = {
        'name': 'Test Aircraft',
        'make': 'Test Make',
        'model': 'Test Model',
        'tail_number': 'TEST123'
    }
    client.post('/api/aircraft', json=data)

    response = client.delete('/api/aircraft/1')
    assert response.status_code == 200

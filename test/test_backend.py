import requests
from mock import get_mock_data
from datetime import datetime

BACKEND_URL = 'http://localhost:5000'

def test_backend_is_reachable():
    res = requests.get(BACKEND_URL)
    assert res.status_code == 200

def test_lookup():
    res = requests.get(BACKEND_URL + '/measurement/lookup')
    assert res.status_code == 200

def clean_database():
    res = requests.get(BACKEND_URL + '/measurement/lookup', {'page_size': -1})
    assert res.status_code == 200
    data = res.json()
    assert 'results' in data
    assert type(data['results']) == list
    for result in data['results']:
        res = requests.delete(
            BACKEND_URL + '/measurement/delete/' + result['_id'])
        assert res.status_code == 200

def test_clean_database():
    clean_database()
    res = requests.get(BACKEND_URL + '/measurement/lookup')
    assert res.status_code == 200
    data = res.json()
    assert 'results' in data
    assert len(data['results']) == 0

def test_create_with_mock_data():
    mock_data = get_mock_data()
    for document in mock_data:
        res = requests.post(BACKEND_URL + '/measurement/submit', json=document)
        if res.status_code == 200:
            print(res.text)
        if res.status_code != 200:
            # Ignore duplicate key error (expected error)
            if 'Duplicate keys' not in res.text:
                if 'Attempted insert' not in res.text:
                    assert res.status_code == 200
    res = requests.get(BACKEND_URL + '/measurement/lookup', {'page_size': -1})
    assert res.status_code == 200
    data = res.json()
    assert 'results' in data
    assert len(data['results']) > 0

def test_create_and_read():
    document = {
        'measurement': 'testing',
        'time': datetime.now().isoformat(),
        'value': 1.0,
        'apid': 100,
    }
    res = requests.post(BACKEND_URL + '/measurement/submit', json=document)
    assert res.status_code == 200
    data = res.json()
    assert '_id' in data
    _id = data['_id']
    res = requests.get(BACKEND_URL + '/measurement/fetch/' + str(_id))
    assert res.status_code == 200
    data = res.json()
    assert 'result' in data
    assert data['result']['value'] == 1

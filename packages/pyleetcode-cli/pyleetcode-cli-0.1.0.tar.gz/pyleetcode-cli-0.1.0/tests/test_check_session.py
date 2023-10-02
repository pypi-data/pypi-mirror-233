import pytest
from leetcode.configuration import check_session_response, check_session_validity, update_session_id
import os
import tempfile
import yaml
import requests_mock

@pytest.fixture
def temp_config_file():
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, 'temp_config.yaml')

    yaml_data = {
        'user_data': {
            'csrv_token': 'example_token',
            'session_id': 'example_session_id',
            'username': 'coderbeep'
        }
    }

    with open(temp_file_path, 'w') as temp_file:
        yaml.dump(yaml_data, temp_file, default_flow_style=False)
    print(temp_file_path)
    return temp_file_path  # Provide the temporary file path to the tests

@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m
        
def test_valid_session(mock_requests):
    mock_requests.post('https://leetcode.com/graphql', json={'data': {'user': {'username': None, 'isCurrentUserPremium': False}}})

    session_id = 'valid_session_id'
    result = check_session_response(session_id)
    assert result is True

def test_invalid_session(mock_requests):
    mock_requests.post('https://leetcode.com/graphql', json={'data': {'user': None}})

    session_id = 'invalid_session_id'
    result = check_session_response(session_id)
    assert result is False
    
def test_update_session_id(temp_config_file):
    update_session_id('new_session_id', temp_config_file)
    with open(temp_config_file, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
    assert data['user_data']['session_id'] == 'new_session_id'

def test_check_session_validity(temp_config_file, monkeypatch):
    monkeypatch.setattr('leetcode.configuration.check_session_response', lambda x: True)
    monkeypatch.setattr('builtins.input', lambda x: 'new_session_id')
    
    monkeypatch.setattr('leetcode.configuration.update_session_id', lambda x: None)
    assert check_session_validity(temp_config_file) is True

def test_check_session_validity_with_invalid_session_id(temp_config_file, monkeypatch):
    # Mocking the check_session_response function to always return False
    counter = 0
    def mock_check_session_response(session_id):
        nonlocal counter
        if counter < 3:
            counter += 1
            return False
        else:
            return True
    monkeypatch.setattr('leetcode.configuration.check_session_response', mock_check_session_response)

    # Mocking the input function to return a specific value
    monkeypatch.setattr('builtins.input', lambda x: 'new_session_id')

    # Mocking the update_session_id function to just pass
    monkeypatch.setattr('leetcode.configuration.update_session_id',  lambda x: None)

    # Import and call the check_session_validity function
    assert check_session_validity(temp_config_file)
# cases: 
# 1. session_id is empty
# 2. session_id is valid
# 3. session_id is invalid
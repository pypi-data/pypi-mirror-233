import argparse
import os
import tempfile

import pytest
import yaml

from leetcode.configuration import \
    UserConfig 


# fixture for temporary config file
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

    return temp_file_path  # Provide the temporary file path to the tests

# fixture for UserConfig object with temporary config file
@pytest.fixture
def user_config_with_temp_file(temp_config_file: str):
    return UserConfig(config_path=temp_config_file)

# Test UserConfig initialization
def test_userconfig_init(temp_config_file: str):
    user_config = UserConfig(config_path=temp_config_file)
    assert user_config.path == temp_config_file
    assert user_config.data is not None

# Test UserConfig get method
def test_userconfig_get(temp_config_file: str):
    user_config = UserConfig(config_path=temp_config_file)
    assert user_config.get('csrv_token') == 'example_token'

# Test UserConfig dump_key method
def test_userconfig_dump_key(temp_config_file: str):
    user_config = UserConfig(config_path=temp_config_file)
    
    user_config.dump_key('new_key', 'new_value')
    
    with open(temp_config_file, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
    assert data['user_data']['new_key'] == 'new_value'

# Test UserConfig execute method with valid args
def test_userconfig_execute_valid_args(user_config_with_temp_file: UserConfig, capsys: pytest.CaptureFixture[str]):
    args = argparse.Namespace(config_key='csrv_token', config_value='new_token')
    user_config_with_temp_file.execute(args)

    # Check if the configuration is updated and a success message is printed
    assert user_config_with_temp_file.get('csrv_token') == 'new_token'
    captured = capsys.readouterr()
    assert "Configuration updated successfully." in captured.out

# Test UserConfig execute method with invalid config_key
def test_userconfig_execute_invalid_key(user_config_with_temp_file: UserConfig, capsys: pytest.CaptureFixture[str]):
    args = argparse.Namespace(config_key='invalid_key', config_value='new_value')
    user_config_with_temp_file.execute(args)

    # Check if an error message is printed for an invalid key
    captured = capsys.readouterr()
    assert "Invalid key: invalid_key" in captured.out
    
# argparse module handles the case when either of the arguments is missing
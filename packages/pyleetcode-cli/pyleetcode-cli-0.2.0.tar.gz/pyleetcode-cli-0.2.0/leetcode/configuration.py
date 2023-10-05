import os
import sys

import requests
import yaml
from rich import print

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, 'config.yaml')
# TODO: logs for changes made to config file
class UserConfig():
    def __init__(self, config_path = CONFIG_PATH) -> None:
        self.path = config_path
        self.data = None
        with open(self.path, 'r') as yaml_file:
            self.data = yaml.safe_load(yaml_file)
        
    def get(self, key):
        return self.data['user_data'].get(key)

    def dump_key(self, key, value):
        self.data['user_data'][key] = value
        
        with open(self.path, 'w') as yaml_file:
            yaml.dump(self.data, yaml_file, default_flow_style=False)

    def _execute(self, args):
        if args.config_key not in self.data['user_data']:
            print(f"Invalid key: {args.config_key}")
            return
        else:
            if getattr(args, 'config_key') and getattr(args, 'config_value'):
                self.dump_key(args.config_key, args.config_value)
                print('[green]Configuration updated successfully.')
              
def check_session_response(session_id: str) -> bool:
    QUERY = """ query
            {
                user {
                username
                isCurrentUserPremium
                }
            }
            """
    response = requests.post(url="https://leetcode.com/graphql",
                                json={'query': QUERY},
                                cookies={'LEETCODE_SESSION': session_id})
    if response.json()['data']['user']:
        return True
    else:  
        return False

def update_session_id(session_id: str, path = CONFIG_PATH):
    with open(path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
    
    data['user_data']['session_id'] = session_id
    with open(path, 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)

def check_session_validity(path = CONFIG_PATH) -> bool:
    with open(path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
    
    SESSION_ID = data['user_data']['session_id']
    while not check_session_response(SESSION_ID):
        SESSION_ID = input("Please provide the proper SESSION_ID: ")
    update_session_id(SESSION_ID)
    return True

""" The main configuration class for the connection to GraphQL API.
    Contains the cookies and headers for the connection.
    
    session_id can be found in the web browser cookies of https://leetcode.com/
    
    The default session_id is taken from the configuration file. """

class Configuration():
    def __init__(self, session_id: str = ''):
        self.host = 'https://leetcode.com'
        self.user_config = UserConfig()
        if session_id:
            self.session_id = session_id
        else:
            self.load_config()
        
        self._csrf_cookie: str = self.csrf_cookie
        
        self._headers: dict = {'x-csrftoken': self._csrf_cookie,
                               'Referer': self.host}
        self._cookies: dict = {'csrftoken': self._csrf_cookie,
                               'LEETCODE_SESSION': self.session_id}  
    
    def check_session_validity(self):
        QUERY = """ query
                {
                    user {
                    username
                    isCurrentUserPremium
                    }
                }
                """
        PARAMETERS = {}
        response = requests.post(url="https://leetcode.com/graphql",
                                    headers=self.headers,
                                    json={'query': QUERY, 'variables': PARAMETERS},
                                    cookies=self.cookies)
        if response.json()['data']['user']:
            Configuration.session_checked = True
        else:
            print('[red]Invalid session_id. Please update the session_id in the config.yaml file or use the config command.[/red]')
            sys.exit(1)
                                 
    
    @property
    def csrf_cookie(self) -> str:
        response = requests.get(url=self.host,
                                cookies={"LEETCODE_SESSION": self.session_id})
        return response.cookies["csrftoken"]
    
    @csrf_cookie.setter
    def csrf_cookie(self, value: str):
        self._csrf_cookie = value
        
    @property
    def headers(self) -> dict:
        return self._headers
    
    @property
    def cookies(self) -> dict:
        return self._cookies
    
    def load_config(self):
        self.session_id = self.user_config.get('session_id')
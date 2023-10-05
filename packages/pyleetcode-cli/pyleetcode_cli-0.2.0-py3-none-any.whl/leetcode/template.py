from leetcode.GQL_parse import Parser
from leetcode.configuration import Configuration
from leetcode.leet_api import LeetAPI
import os

class QueryTemplate():
    session_checked =  False
    
    def __init__(self):
        self.config = Configuration()
        if not QueryTemplate.session_checked:
            self.config.check_session_validity()
            
        self.leet_API = LeetAPI(self.config)
        self.parser = Parser()
        
        self.params = None
        
        self.query_name = None
        
        self.query = None
        
        self.get_name()
        self.get_query()
    
    def show(self):
        """ Basic information showing functionality. """
        pass
    
    def get_name(self):
        self.query_name = self.__class__.__name__

    def get_query(self):
        self.query = self.parser.extract_query(self.query_name)

    def execute(self, args):
        """ 
        Method to handle the args passed by the argument parser. Fetches the data
        and displays it in the terminal.

        Args:
            args (argparse.Namespace): A list of arguments passed by the argument parser.

        Returns:
            None
        """
        pass

    def open_in_browser(self, link):
        """ Method to open the question in browser. """
        os.system(f'explorer {link}')
        pass
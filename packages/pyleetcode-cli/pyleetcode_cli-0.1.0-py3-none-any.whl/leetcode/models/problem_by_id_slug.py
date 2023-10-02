from leetcode.configuration import Configuration
from leetcode.leet_api import LeetAPI
from leetcode.models import *
from leetcode.models.graphql_get_question_detail import GetQuestionDetail
from leetcode.models.graphql_question_content import QuestionContent
from leetcode.models.graphql_question_info_table import QuestionInfoTable
from leetcode.models.graphql_problemset_question_list import ProblemTotalCount, ProblemsetQuestionList


class ProblemInfo(QueryTemplate):
    API_URL = "https://leetcode.com/api/problems/all/"
    configuration = Configuration()
    leet_api = LeetAPI(configuration)
    
    def __init__(self):
        super().__init__()
        # Instance specific variables
        self.browserFlag = False
        self.fileFlag = False
        
        self._question_id: int = None
        self._title_slug: str = None
        self._data = None

    @classmethod
    def get_title_slug(cls, question_id: int) -> str:
        """ Returns the title slug of the problem with the given ID.
        
        Args:
            question_id (int): The ID of the problem.
            
        Returns:
            str: The title slug of the problem with the given ID."""
        response = cls.leet_api.get_request(cls.API_URL)
        for item in response.get('stat_status_pairs', []):
            if item['stat'].get('question_id') == question_id:
                return item['stat'].get('question__title_slug', '')
        else:
            raise ValueError("Invalid ID has been provided. Please try again.")
    
    @classmethod
    def get_id(cls, title_slug: str) -> int:
        """ Returns the ID of the problem with the given slug.
        
        Args:
            title_slug (str): The title slug of the problem.
            
        Returns:
            int: The ID of the problem with the given slug."""
        response = cls.leet_api.get_request(cls.API_URL)
        for item in response.get('stat_status_pairs', []):
            if item['stat'].get('question__title_slug') == title_slug:
                return item['stat'].get('question_id', 0)
        else:
            raise ValueError("Invalid slug has been provided. Please try again.")
        
    @classmethod    
    def lookup_slug(cls, question_slug: str): 
        """ Checks if the given slug is valid. 
        
        Args:
            question_slug (str): The slug to check.
        
        Returns:
            bool: True if the slug is valid, False otherwise."""
        response = cls.leet_api.get_request(cls.API_URL)
        for item in response.get('stat_status_pairs', []):
            if item['stat'].get('question__title_slug') == question_slug:
                return True
        raise ValueError("Invalid slug has been provided. Please try again.")

    def fetch_data(self, question_id: str):
        """ Fetches the question data for the given question ID. 
        Args:
            question_id (str): The question ID to fetch data for. 
        """
        try:
            if question_id is not None and question_id != self.question_id:
                self.question_id = question_id
            
            self.data = self.data if self.data is not None else self.leet_api.get_request(self.API_URL)
            self.show()
        except Exception as e:
            console.print(f"{e.__class__.__name__}: {e}", style=ALERT)
            sys.exit(1)

    def _execute(self, args):
        """ Executes the query with the fiven arguments and displays the result. 
        
        Args:
            args (argparse.Namespace): The arguments passed to the query."""
        self.__parse_args(args)          
        if getattr(args, 'random'):
            total = ProblemTotalCount({'status': 'NOT_STARTED'}).__call__()
            from random import randint
            with Loader('Selecting random problem...', ''):
                choosen_number = randint(1, total)
                while True:
                    list_instance = ProblemsetQuestionList({'status': 'NOT_STARTED'}, limit=1, skip=choosen_number - 1)
                    problem = list_instance.fetch_data()['problemsetQuestionList']['questions'][0]
                    if not problem['paidOnly']:
                        break
                    choosen_number = randint(1, total)

            with Loader('Fetching problem contents...', ''):
                question_info_table = QuestionInfoTable(problem['titleSlug'])
                question_content = QuestionContent(problem['titleSlug'])
            console.print(question_info_table)
            console.print(question_content)
            
        else:
            try:
                with Loader('Fetching problem info...', ''):
                    self.data = self.leet_api.get_request(self.API_URL)
                    if getattr(args, 'id'):
                        for item in self.data.get('stat_status_pairs', []):
                            if item['stat'].get('question_id') == args.id:
                                self.title_slug = item['stat'].get('question__title_slug', '')
                                break
                        if not self.title_slug:
                            raise ValueError("Invalid ID has been provided. Please try again.")
                self.show()
            except Exception as e:
                console.print(f"{e.__class__.__name__}: {e}", style=ALERT)
            if self.fileFlag:
                self.create_submission_file(self.title_slug)
    
    @classmethod
    def create_submission_file(cls, title_slug: str = None) -> None:
        """ Creates a file with the problem content. 
        The file is named as follows: <question_id>.<question_title_slug>.py
        
        Args:
            title_slug (str): The title slug of the problem.
        """
        question = GetQuestionDetail(title_slug)
        file_name = f"{question.question_id}.{question.title_slug}.py"
        with open(file_name, 'w') as file:
            file.write(question.code_snippet)
        console.print(f"File '{file_name}' has been created.")
           
    def show(self):
        if self.browserFlag:
            question_info_table = QuestionInfoTable(self.title_slug)
            console.print(question_info_table)
            link = self.config.host + f'/problems/{self.title_slug}/'
            console.print(f'Link to the problem: {link}')
            self.open_in_browser(link)
        else:
            question_info_table = QuestionInfoTable(self.title_slug)
            console.print(question_info_table)
            question_content = QuestionContent(self.title_slug)
            console.print(question_content)

    def __parse_args(self, args) -> None:
        """ Parses the arguments passed to the query. 
        
        Args:
            args (argparse.Namespace): The arguments passed to the query. """
        if getattr(args, 'browser'): 
            self.browserFlag = True
        if getattr(args, 'file'):
            self.fileFlag = True
            
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, data: Dict):
        self._data = data
        
    @property
    def title_slug(self):
        return self._title_slug
    
    @title_slug.setter
    def title_slug(self, title_slug: str):
        self._title_slug = title_slug
        
    @property
    def question_id(self):
        return self._question_id
    
    @question_id.setter
    def question_id(self, question_id: int):
        self._question_id = question_id
        self.title_slug = self.get_title_slug(question_id)
        
if __name__ == '__main__':
    info = ProblemInfo()
    info.fetch_data(1)
    
    info.fetch_data(2)
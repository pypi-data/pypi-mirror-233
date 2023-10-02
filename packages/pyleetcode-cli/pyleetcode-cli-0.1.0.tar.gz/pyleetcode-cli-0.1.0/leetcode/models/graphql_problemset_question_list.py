from leetcode.models import *

""" This module contains the QueryTemplate class for the problemsetQuestionList query. 
    The class is used to fetch a list of LeetCode problems by the 'list' command.
    """

@dataclass
class QueryResult(JSONWizard):
    @dataclass
    class Question():
        title: str
        status: str
        difficulty: str
        frontendQuestionId: int
        questionId: int
    total: int
    questions: List[Question]
    
    @classmethod
    def from_dict(cls, data):
        total = data['problemsetQuestionList']['total']
        questions_data = data['problemsetQuestionList']['questions']
        questions = [
            cls.Question(
                title=item.get('title'),
                status=item.get('status'),
                difficulty=item.get('difficulty'),
                frontendQuestionId=item.get('frontendQuestionId'),
                questionId=item.get('questionId')
            )
            for item in questions_data
        ]
        return cls(total=total, questions=questions)
    
class ProblemTotalCount(QueryTemplate):
    def __init__(self, filters={}):
        super().__init__()
        self.graphql_query = None
        self.result = None
        self.params = {'categorySlug': '', 'filters': filters}
        
        self.execute()
        
    def execute(self):
        self.graphql_query = GraphQLQuery(self.query, self.params)
        self.result = self.leet_API.post_query(self.graphql_query)
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.result['data']['problemsetQuestionList']['total']


class ProblemsetQuestionList(QueryTemplate):
    """ A class to represent a list of LeetCode problems.

    Args:
        filters (dict, optional): Filters to apply to the query. Defaults to {}. 
            - 'difficulty' (str, optional): Difficulty level. Valid values: 'EASY', 'MEDIUM', 'HARD'.
            - 'status' (str, optional): Status of the problem. Valid values: 'NOT_STARTED', 'TRIED', 'AC'.
        limit (int, optional): Maximum number of problems to retrieve. Defaults to None.
            If not provided, the value is taken from the user config file.
        skip (int, optional): Number of problems to skip. Defaults to 0.
    """

    def __init__(self, filters={}, limit=None, skip=0):
        super().__init__()
        # Instance specific variables
        self.page : int = 1
        self.max_page : int = 0
        self.filters = filters
        self.limit = limit or self.config.user_config.get('question_list_limit')
        self.skip = skip
        self._data_fetched: bool = False
        
        self._params = {'categorySlug': "", 
                       'skip':self.skip, 
                       'limit': self.limit, 
                       'filters': self.filters}

        self.data = None
        
    def fetch_data(self, parameters: Dict) -> QueryResult:
        """ Fetches the data from the LeetCode API. 
            Updates the state of the object.

        Args:
            parameters (dict, optional): Parameters to pass to the query. Defaults to None.

        Returns:
            QueryResult: The result of the query.
        """
        try: 
            with Loader('Fetching problems...', ''):
                if parameters is not None and parameters != self.params:
                    self.params = parameters
                
                if self.data_fetched:
                    return self.data
            
                self.graphql_query = GraphQLQuery(self.query, parameters)
                self.data = self.leet_API.post_query(self.graphql_query) # Take the response from the API
                self.data = QueryResult.from_dict(self.data['data'])
                self.data_fetched = True
                return self.data
        except Exception as e:
            console.print(f"{e.__class__.__name__}: {e}", style=ALERT)
            sys.exit(1)
        
    def _execute(self, args):
        """ Executes the query with the given arguments and displays the result.

        Args:
            args (argparse.Namespace): The arguments passed to the query.
        """

        self.__parse_args(args)
        self.data = self.fetch_data(self.params)
        self.show()

    def show(self) -> None:
        """ Displays the query result in a table.

        Args:
            query_result (QueryResult, optional): The result of the query. Defaults to None.
                If the result is None, the method will try to fetch the data with defauly parameters and than display it.
        """
        if self.data_fetched:   
            displayed : int = self.limit * self.page if self.limit * self.page < self.data.total else self.data.total
            
            table = LeetTable(title=f'Total number of problems retrieved: {self.data.total}\n',
                                caption=f"Page #{self.page} / ({displayed}/{self.data.total})")
            
            table.add_column('ID')
            table.add_column('Title')
            table.add_column('Status')
            table.add_column('Difficulty')
            for item in self.data.questions:
                table.add_row(item.questionId, item.title, item.status, item.difficulty)
            console.print(table)
        else:
            raise Exception("Data is not fetched yet.")
    
    def __validate_page(self):
        """ Validates the current page number.
        If the number is too large, sets the page number to the last page.
        """

        count = ProblemTotalCount().__call__()
        self.page = min(self.page, -(-count // self.limit))
        self.params['skip'] = self.limit * self.page - self.limit # update the skip value

    def __parse_args(self, args):
        """ Parses the arguments passed to the query.

        Args:
            args (argparse.Namespace): The arguments passed to the query.
        """
        
        # Parse status argument
        status_mapping = {"solved": "AC",
                            "todo": "NOT_STARTED",
                            "attempted": "TRIED"}
        status_argument = None
        for status_arg in status_mapping.keys():
            if getattr(args, status_arg):
                status_argument = status_arg
                break
            
        if status_argument is not None:
            self.params['filters']['status'] = status_mapping[status_argument]
            
        # Parse the page argument
        self.page = getattr(args, 'page') 
        self.params['skip'] = self.limit * self.page - self.limit
        
        self.__validate_page()
        
    @property
    def data_fetched(self):
        return self._data_fetched
    
    @data_fetched.setter
    def data_fetched(self, data_fetched: bool):
        self._data_fetched = data_fetched
    
    @property
    def params(self):
        return self._params
    
    @params.setter
    def params(self, params: dict):
        self._params = params
        self.data_fetched = False
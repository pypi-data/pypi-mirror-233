from datetime import datetime, timedelta

from leetcode.models import *


# TODO: Add the submission ID into the table, so that the user can copy paste that to download the submitted code
@dataclass
class MatchedUser:
    @dataclass
    class DifficultyPercentage:
        # when the leetcode account does not have enough completed exercises
        # the percentage is not calculated, hence the 'Optional' part
        difficulty: str
        percentage: Optional[float]
        
    @dataclass
    class DifficultySubmission:
        difficulty: str
        count: int
    
    problemsSolvedBeatsStats: List[DifficultyPercentage]
    submitStatsGlobal: Dict[str, List[DifficultySubmission]]

@dataclass
class QueryResult(JSONWizard):
    @dataclass
    class DifficultyCount:
        difficulty: str
        count: int
    
    allQuestionsCount: List[DifficultyCount] # questions count according to difficulty
    matchedUser: MatchedUser
    
class UserProblemsSolved(QueryTemplate):
    """ A class to represent user's LeetCode statistics. """
    
    def __init__(self):
        super().__init__()
        # Instance specific variables
        self._username: str = None
        
        self._params = {'username': ''}
        self._data = None
        self._data_fetched: bool = False
        
    def fetch_data(self, username: str) -> Dict:
        """ Fetches the user's LeetCode statistics.
        
        Args:
            username (str): The username of the user.
            
        Returns:
            Dict: The user's LeetCode statistics.
        """
        try:
            with Loader('Fetching user stats...', ''):
                if username != None and username != self.username:
                    self.username = username
                
                if self.data_fetched:
                    return self.data
                
                graphql_query = GraphQLQuery(self.query, self.params)
                response = self.leet_API.post_query(graphql_query)
                if 'errors' in response:
                    raise Exception(response['errors'][0]['message'])
                self.data = QueryResult.from_dict(response['data'])
                self.data_fetched = True
                return self.data
        except Exception as e:
            console.print(f"{e.__class__.__name__}: {e}", style=ALERT)
            sys.exit(1)
    
    def _execute(self, args) -> None:
        """ Executes the query with the given arguments and displays the result. 
        
        Args:
            args (argparse.Namespace): The arguments passed to the query. """
        try:
            with Loader('Fetching user stats...', ''):            
                self.__parse_args(args)
                
                self.graphql_query = GraphQLQuery(self.query, self.params)
                self.data = self.leet_API.post_query(self.graphql_query)
                if 'errors' in self.data:
                    raise Exception(self.data['errors'][0]['message'])
                self.data = QueryResult.from_dict(self.data['data'])
            self.show()
        except Exception as e:
            console.print(f"{e.__class__.__name__}: {e}", style=ALERT)
    
    def show_stats(self) -> None:
        """ Displays the user's LeetCode questions count. """
        
        difficulties = [x.difficulty for x in self.data.allQuestionsCount]
        question_counts = [x.count for x in self.data.allQuestionsCount]
        beaten_stats = [x.percentage for x in self.data.matchedUser.problemsSolvedBeatsStats]
        beaten_stats.insert(0, None)
        submit_counts = []
        for diff, subm in self.data.matchedUser.submitStatsGlobal.items():
            for submission in subm:
                submit_counts.append(submission.count)
        
        table = LeetTable(title=f"{self.username}'s Leetcode Stats")
        table.add_column('Difficulty')
        table.add_column('Question Count')
        table.add_column('Beaten Stats (%)')
        table.add_column('Submit Count')
        
        for diff, count, stats, subm in zip(difficulties, question_counts, beaten_stats, submit_counts):
            table.add_row(diff, str(count), str(stats), str(subm)) 
        console.print(table)
    
    def show(self) -> None:
        """ Displays information about the user's LeetCode statistics. """
        
        self.show_stats()
        self.recent_submissions()

    @staticmethod
    def time_ago(timestamp: int) -> str:
        """ Returns the time difference between the current time and the given timestamp. 
        
        Args:
            timestamp (int): The timestamp to compare with.
        
        Returns:
            str: The time difference between the current time and the given timestamp. 
        """
        current_time = datetime.now()
        timestamp_time = datetime.fromtimestamp(timestamp)
        time_difference = current_time - timestamp_time

        if time_difference < timedelta(minutes=1):
            return "just now"
        elif time_difference < timedelta(hours=1):
            minutes = time_difference.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif time_difference < timedelta(days=1):
            hours = time_difference.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif time_difference < timedelta(weeks=1):
            days = time_difference.days
            return f"{days} day{'s' if days != 1 else ''} ago"
        else:
            weeks = time_difference.days // 7
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"

    def recent_submissions(self) -> None:
        """ Displays the user's recent submissions in a table. 
        The table contains the submission ID, the problem title and the time when the submission was made."""
        with Loader('Fetching recent submissions...', ''):
            self.submissions_query = self.parser.extract_query('recentAcSubmissions')
            self.subm_params = {'username': self.params['username'], 'limit': 10}
            self.subm_result = self.leet_API.post_query(GraphQLQuery(self.submissions_query, self.subm_params))
            self.subm_result = self.subm_result['data']['recentAcSubmissionList']

            self.id_query = self.parser.extract_query('GetQuestionId')
            
            table = LeetTable(title='Recent Submissions', width = 70)
            table.add_column('ID')
            table.add_column('Title')
            table.add_column('Time')
            
            for subm in self.subm_result:
                self.subm_params = {'titleSlug': subm['titleSlug']}
                question_id = self.leet_API.post_query(GraphQLQuery(self.id_query, self.subm_params))['data']['question']['questionId']
                table.add_row(question_id, subm['title'], self.time_ago(int(subm['timestamp'])))

        print(table)
        

    def __parse_args(self, args):
        """ Parses the arguments passed to the query. 
        
        Args:
            args (argparse.Namespace): The arguments passed to the query.
        """
        if getattr(args, 'username'):
            self.params['username'] = getattr(args, 'username')
        else:
            self.username = self.config.user_config.get('username')
            if self.username:
                self.params['username'] = self.config.user_config.get('username')
            else:
                console.print("Username neither provided nor configured. Head to --help.", style=ALERT)
                sys.exit(1)

    @property
    def username(self) -> str:
        return self._username
    
    @username.setter
    def username(self, username: str) -> None:
        self._username = username
        self.data_fetched = False
        self.params['username'] = username
    
    @property
    def data_fetched(self) -> bool:
        return self._data_fetched
    
    @data_fetched.setter
    def data_fetched(self, value: bool) -> None:
        self._data_fetched = value
        
    @property
    def data(self) -> Dict:
        return self._data
    
    @data.setter
    def data(self, data: Dict) -> None:
        self._data = data
        
    @property
    def params(self) -> Dict:
        return self._params
    
    @params.setter
    def params(self, params: Dict) -> None:
        self._params = params
        self.data_fetched = False
        
# if __name__ == '__main__':
#     stats = UserProblemsSolved()
#     stats.fetch_data('skygragon')
#     stats.show()
    
#     stats.fetch_data('coderbeep')
#     stats.show()
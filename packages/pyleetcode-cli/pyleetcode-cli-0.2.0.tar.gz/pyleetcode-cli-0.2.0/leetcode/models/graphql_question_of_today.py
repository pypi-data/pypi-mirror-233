from leetcode.models import *
from leetcode.models.graphql_question_content import QuestionContent
from leetcode.models.graphql_question_info_table import QuestionInfoTable
from leetcode.models.graphql_get_question_detail import GetQuestionDetail

@dataclass
class QueryResult(JSONWizard):
    @dataclass
    class Question():
        difficulty: str
        status: str
        title: str
        titleSlug: str
        frontendQuestionId: int
        
    date: str
    userStatus: str
    link: str
    question: Question
    
    @classmethod
    def from_dict(cls, data):
        date = data['activeDailyCodingChallengeQuestion']['date']
        userStatus = data['activeDailyCodingChallengeQuestion']['userStatus']
        link = data['activeDailyCodingChallengeQuestion']['link']
        
        
        question = data['activeDailyCodingChallengeQuestion']['question']
        question = cls.Question(title=question.get('title'),
                             status=question.get('status'),
                             titleSlug=question.get('titleSlug'),
                             difficulty=question.get('difficulty'),
                             frontendQuestionId=question.get('frontendQuestionId'))
        
        return cls(date=date, userStatus=userStatus, link=link, question=question)  

class QuestionOfToday(QueryTemplate):
    """ A class representing the LeetCode question of the day. """
    def __init__(self):
        super().__init__()
        # Instance specific variables
        self.contentFlag: bool = False
        self.browserFlag: bool = False
        self.fileFlag: bool = False
        self.title_slug: str = None
    
        self.data = None
        
    def fetch_data(self) -> Dict:
        """ Fetches the question of the day data.

        Returns:
            Dict: The question of the day data.
        """
        try:
            with Loader('Fetching question of the day...', ''):
                graphql_query = GraphQLQuery(self.query, {})
                response = self.leet_API.post_query(graphql_query)
                return response['data']
        except Exception as e:
            console.print(f"{e.__class__.__name__}: {e}", style=ALERT)
            sys.exit(1)
    
    def _execute(self, args) -> None:
        """ Executes the query with the given arguments and displays the result.

        Args:
            args (argparse.Namespace): The arguments passed to the query.
        """
        with Loader('Fetching question of the day...', ''):
            self.__parse_args(args)
            
            self.graphql_query = GraphQLQuery(self.query, {})
            self.data = self.leet_API.post_query(self.graphql_query)
            self.data = QueryResult.from_dict(self.data['data'])
            self.title_slug = self.data.question.titleSlug
            
        self.show()
        
        if self.fileFlag:
            self.create_submission_file(self.title_slug)

    def show(self) -> None:
        """ Shows the question information and content or opens the question in a browser. 
        The displayed information depends on the flags passed to the command line.
        """
        question_info_table = QuestionInfoTable(self.title_slug)
        if self.contentFlag:
            print(question_info_table)
            print('\n')
            question_content = QuestionContent(self.title_slug)
            print(question_content)
        elif self.browserFlag:
            print(question_info_table)
            link = self.config.host + self.data.link
            print(f'Link to the problem: {link}')
            self.open_in_browser(link)
        else:
            print(question_info_table)
    
    @classmethod      
    def create_submission_file(cls, title_slug: str) -> None:
        """ Creates a file with the question content. 
        
        Args:
            title_slug (str): The title slug of the question. """
            
        """ Add watermark to the file."""
        watermark_info = '# This file was created by pyleetcode-cli software.\n# Do NOT modify the name of the file.\n\n'
        question = GetQuestionDetail(title_slug)
        filename = f"{question.question_id}.{question.title_slug}.py"
        with open(filename, 'w') as file:
            file.write(watermark_info)
            file.write(question.code_snippet)
        console.print(f"File '{filename}' has been created.")
        
    def __parse_args(self, args) -> None:
        """ Parses the command line arguments.

        Args:
            args (argparse.Namespace): The command line arguments.
        """
        if getattr(args, 'browser'): 
            self.browserFlag = True
        if getattr(args, 'contents'):
            self.contentFlag = True
        if getattr(args, 'file'):
            self.fileFlag = True
        


        
    

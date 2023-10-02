import requests

from leetcode.models import *
from leetcode.models.graphql_get_question_detail import GetQuestionDetail
from leetcode.models.problem_by_id_slug import ProblemInfo


# TODO: Add a decorator to check if the user is logged in
# Example output of check/ for the success
class SendSubmission(QueryTemplate):
    def __init__(self):
        super().__init__()
        self.title_slug = None
        self.path = None
        self.runcode = None
        self.submission_id = None
        
        self.submit_response = None

    @property
    def submit_url(self):
        return f"https://leetcode.com/problems/{self.title_slug}/submit/"
    
    @property
    def submit_check_url(self):
        return f"https://leetcode.com/submissions/detail/{self.submission_id}/check/"
    
    @property
    def interpret_url(self):
        return f"https://leetcode.com/problems/{self.title_slug}/interpret_solution/"
    
    @property
    def runcode_check_url(self):
        return f"https://leetcode.com/submissions/detail/{self.runcode}/check/"
    
    def parse_args(self, args):
        self.title_slug = args.question_slug
        self.path = args.path
        
        # check if such slug exists
        ProblemInfo.lookup_slug(self.title_slug)
        
    def _execute(self, args):
        try:
            with Loader('Uploading submission...', ''):
                self.parse_args(args)
                self.execute_submission(self.title_slug, self.path)
            
            self.show_submission_info(self.submit_response)
        except Exception as e:
            console.print(f"{e.__class__.__name__}: {e}", style=ALERT)
    
    def load_code(self, filename):
        with open(filename, 'r') as file:
            code = file.read()
        
        if code == '':
            raise Exception("File is empty")
        
        return code
    
    def execute_check(self, title_slug, filename):
        question = GetQuestionDetail(title_slug)
        self.params = {"lang": "python3",
                       "question_id": question.question_id,
                       "typed_code": self.load_code(filename),
                       "data_input": question.sample_test_case}
        
        # Interpret solution
        response = requests.post(url=self.interpret_url,
                                 headers=self.config.headers,
                                 json=self.params,
                                 cookies=self.config.cookies)
        self.runcode = response.json()['interpret_id']
        
        response = requests.get(url=self.runcode_check_url,
                            headers=self.config.headers,
                            cookies=self.config.cookies)
    
        while response.json().get('state') == 'STARTED' or response.json().get('state') == 'PENDING':
            response = requests.get(url=self.runcode_check_url,
                                    headers=self.config.headers,
                                    cookies=self.config.cookies)
        self.show_check_info(response.json())
    
    def show_check_info(self, response):
        if response.get('run_success'):
            print(f"Runtime: {response.get('status_runtime')}")
            print(f"Answer: {response.get('correct_answer')}")
            print(f"Expected: {response.get('expected_code_answer')}")
            print(f"Got answer: {response.get('code_answer')}")
        else:
            print(f"Exception: {response.get('status_msg')}")
            
    def execute_submission(self, title_slug, filename):
        # In similar way execute clicking submit button on the leetcode website
        question = GetQuestionDetail(title_slug)
        self.params = {"lang": "python3",
                    "question_id": question.question_id,
                    "typed_code": self.load_code(filename)}

        # Submit solution
        response = requests.post(url=self.submit_url,
                                headers=self.config.headers,
                                json=self.params,
                                cookies=self.config.cookies)
        self.submission_id = response.json()['submission_id']
        
        response = requests.get(url=self.submit_check_url,
                            headers=self.config.headers,
                            cookies=self.config.cookies)
    
        while response.json().get('state') == 'STARTED' or response.json().get('state') == 'PENDING':
            response = requests.get(url=self.submit_check_url,
                                    headers=self.config.headers,
                                    cookies=self.config.cookies)
        self.submit_response = response.json()
            
    def show_submission_info(self, response):
        if response.get('run_success'):
            status_msg = response.get('status_msg')
            if status_msg == 'Accepted': # If the solution is accepted
                print(f"Status: [bold green]{status_msg}[/bold green] :tada:")
                print(f"Passed {response.get('total_correct')}/{response.get('total_testcases')} test cases -> {response.get('status_runtime')}")

                perc_evalutaion = SubmitEvaluation(f"{response.get('runtime_percentile'):.2f}", f"{response.get('memory_percentile'):.2f}")
                print(perc_evalutaion)
            elif status_msg == 'Wrong Answer': # If the solution is wrong
                print(f"Status: [bold red]{status_msg}[/bold red] :tada:")
                print(f"Passed {response.get('total_correct')}/{response.get('total_testcases')} testcases")
        else:
            if response.get('status_msg') == 'Time Limit Exceeded':
                print(f"Status: [bold red]{response.get('status_msg')}[/bold red] :alarm_clock:")
                print(f"Passed {response.get('total_correct')}/{response.get('total_testcases')} testcases")
            elif response.get('status_msg') == 'Runtime Error':
                print(f"Status: [bold red]{response.get('status_msg')}[/bold red]")
                print(f"{response.get('runtime_error')}")
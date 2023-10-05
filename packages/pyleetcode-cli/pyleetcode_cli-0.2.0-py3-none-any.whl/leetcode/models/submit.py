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
        self.command = None
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
        import os
        self.command = args.command
        self.path = args.path
        
        
        # Get the info from filename : 1234.title-slug.py
        filename = os.path.basename(self.path)
        self.title_slug = filename.split('.')[1]
        
        
        # check if such slug exists
        ProblemInfo.lookup_slug(self.title_slug)
        
    def _execute(self, args):
        try:
            self.parse_args(args)
            if self.command == 'submit':
                with Loader('Uploading submission...', ''):
                    submit_response = self.execute_submission(self.title_slug, self.path)
                self.show_submission_info(submit_response)
            elif self.command == 'check':
                with Loader('Checking submission...', ''):
                    check_response = self.execute_check(self.title_slug, self.path)
                self.show_check_info(check_response)
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
        return response.json()
        
    
    def show_check_info(self, response):
        if response.get('run_success'):
            console.print("\n[bold green]✓ Check Passed[/bold green]\n")
            console.print(f"[bold]Runtime:[/bold] {response.get('status_runtime')}")
            console.print(f"[bold]Answer:[/bold] {response.get('correct_answer')}")
            console.print(f"[bold]Expected:[/bold] {response.get('expected_code_answer')}")
            console.print(f"[bold]Got answer:[/bold] {response.get('code_answer')}")
        else:
            console.print("\n[bold red]✗ Check Failed[/bold red]\n")
            console.print(f"[bold]Exception:[/bold] {response.get('status_msg')}")
            
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
        return response.json()
            
    def show_submission_info(self, response):
        if response.get('run_success'):
            status_msg = response.get('status_msg')
            if status_msg == 'Accepted': # If the solution is accepted
                console.print(f"\n[bold green]✓ Submission Passed[/bold green] :tada:")
                console.print(f"Passed {response.get('total_correct')}/{response.get('total_testcases')} test cases in {response.get('status_runtime')}")

                perc_evalutaion = SubmitEvaluation(f"{response.get('runtime_percentile'):.2f}", f"{response.get('memory_percentile'):.2f}")
                console.print(perc_evalutaion)
            elif status_msg == 'Wrong Answer': # If the solution is wrong
                console.print(f"\n[bold red]✗ Submission Failed[/bold red] :tada:")
                console.print(f"Passed {response.get('total_correct')}/{response.get('total_testcases')} testcases")
        else:
            if response.get('status_msg') == 'Time Limit Exceeded':
                console.print(f"\n[bold red]✗ Submission Failed[/bold red] :alarm_clock:")
                console.print(f"Passed {response.get('total_correct')}/{response.get('total_testcases')} testcases")
            elif response.get('status_msg') == 'Runtime Error':
                console.print(f"\n[bold red]✗ Submission Failed[/bold red]")
                console.print(f"{response.get('runtime_error')}")

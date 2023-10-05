import argparse

# from leetcode.models import *
from leetcode.configuration import UserConfig
from leetcode.models.graphql_problemset_question_list import \
    ProblemsetQuestionList
from leetcode.models.graphql_question_of_today import QuestionOfToday
from leetcode.models.graphql_submission_list import SubmissionList
from leetcode.models.graphql_user_problems_solved import UserProblemsSolved
from leetcode.models.problem_by_id_slug import ProblemInfo
from leetcode.models.submit import SendSubmission

# TODO: pipes support
# TODO: add a command to open the question in editor
# TODO: add a command to show the solution in the terminal
# TODO: add a command to show the solution in the browser
# TODO: problem with import in synced code or code to submit
# TODO: check the changes in question_content and apply them to the code in other files
# TODO: check all commands for errors
# TODO: README - search - download - check - submit

def positive_integer(value):
    try:
        ivalue = int(value)
        if ivalue > 0:
            return ivalue
        else:
            raise argparse.ArgumentTypeError(f"{value} is not a valid integer")
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid integer")

def main():
    parser = argparse.ArgumentParser(description="Leet CLI")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1.0')
    subparsers = parser.add_subparsers(title="Commands", dest="command")
    
    config_parser = subparsers.add_parser('config', help="Configure the CLI")
    config_parser.add_argument('config_key', type=str, help='Key to change')
    config_parser.add_argument('config_value', type=str, help='Value to set') 
    config_parser.set_defaults(func=UserConfig)
    
    stats_parser = subparsers.add_parser("stats", help="Display statistics")
    stats_parser.add_argument('username', type=str, help='User nickname', nargs='?')
    stats_parser.set_defaults(func=UserProblemsSolved)
    
    problems_list_parser = subparsers.add_parser("list", help="Display problem list")
    problems_list_parser.add_argument('page', type=positive_integer, help='Page number', nargs='?', default=1)
    problems_list_parser.set_defaults(func=ProblemsetQuestionList)
    
    group = problems_list_parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--solved', action='store_true', help='Display only solved problems.')
    group.add_argument('-t', '--todo', action='store_true', help='Display only to do.')
    group.add_argument('-a', '--attempted', action='store_true', help='Display only attempted problems.')
    
    problem_parser = subparsers.add_parser('problem', help="Display problem")
    problem_parser.set_defaults(func=ProblemInfo)
    problem_parser.add_argument('-r', '--random', action='store_true', help='Fetch a random problem.')
    problem_parser.add_argument('id', type=positive_integer, help='Problem ID of the problem', default=0, nargs='?')
    problem_parser.add_argument('-b', '--browser', action='store_true', help='Open the page in browser.')
    problem_parser.add_argument('-f', '--file', action='store_true', help='Create a file with the problem content.')
    problem_parser.add_argument('-c', '--contents', action='store_true', help='Display contents of the question in the terminal.')

    
    today_problem_parser = subparsers.add_parser('today', help="Display today's problem.")
    today_problem_parser.set_defaults(func=QuestionOfToday)
    group_2 = today_problem_parser.add_mutually_exclusive_group()
    group_2.add_argument('-b', '--browser', action='store_true', help='Open the page in browser.')
    group_2.add_argument('-c', '--contents', action='store_true', help='Display contents of the question in the terminal.')
    group_2.add_argument('-f', '--file', action='store_true', help='Create a file with the problem content.')
    
    submission_parser = subparsers.add_parser('submission', help="Download submission code")
    submission_parser.add_argument('id', type=int, help='ID of the problem.')
    submission_parser.add_argument('-s', '--show', action='store_true', help='Show latest accepted code in the terminal.')
    submission_parser.add_argument('-d', '--download', action='store_true', help='Download the latest accepted code.')
    submission_parser.set_defaults(func=SubmissionList)
    
    submission_parser = subparsers.add_parser('submit', help='Submit code answer')
    submission_parser.add_argument('path', type=str, help='Path to the file with code answer')
    submission_parser.set_defaults(func=SendSubmission)
    
    submission_parser = subparsers.add_parser('check', help='Check code answer on example test')
    submission_parser.add_argument('path', type=str, help='Path to the file with code answer')
    submission_parser.set_defaults(func=SendSubmission)
        
    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        command_instance = args.func()
        command_instance._execute(args)
    else:
        print("Unknown command. Use 'leet --help' for available commands.")


if __name__ == '__main__':
    main()
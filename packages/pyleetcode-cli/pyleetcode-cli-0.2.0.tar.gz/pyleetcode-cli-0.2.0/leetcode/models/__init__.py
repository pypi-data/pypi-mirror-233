# Import the available models from models folder
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from leetcode.loader import Loader

import rich
from dataclass_wizard import JSONWizard
from rich import print
from rich.console import Console
from rich.table import Table
from .styles import ALERT, LeetTable, SubmitEvaluation

console = Console()

from leetcode.content_markdown import LeetQuestionToSections
from leetcode.graphql_query import GraphQLQuery
from leetcode.template import QueryTemplate

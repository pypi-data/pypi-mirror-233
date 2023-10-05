from leetcode.models import *

class GetQuestionDetail(QueryTemplate):
    """ A class to represent a LeetCode problem. 
    
    Args:
        title_slug (str): The title slug of the problem. 
    """
    def __init__(self, title_slug: str):
        super().__init__()
        # Instance-specific variables
        self._title_slug = title_slug
        self._data = None
        self._params = {'titleSlug': title_slug}
        self._data_fetched: bool = False

        self.fetch_data()

    def fetch_data(self, title_slug: str = None) -> Dict:
        """ Fetches the data for the problem. 
        
        Args:
            parameters (dict, optional): Parameters to pass to the query. Defaults to None.
        
        Returns:
            Dict: The data for the problem.
        """
        try:
            with Loader('Fetching question details...', ''):
                if title_slug is None:
                    parameters = self.params
                elif title_slug != self.title_slug:
                    self.title_slug = title_slug
                    self.params = {'titleSlug': title_slug}
                    parameters = self.params
                if self.data_fetched:
                    return self._data

                graphql_query = GraphQLQuery(self.query, parameters)
                response = self.leet_API.post_query(graphql_query)
                if 'errors' in response:
                    raise Exception(response['errors'][0]['message'])
                self.data = response['data']['question']
                self.data_fetched = True
                self.params = parameters
                return self.data
        except Exception as e:
            console.print(f"{e.__class__.__name__}: {e}", style=ALERT)
            sys.exit(1)
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, data: dict):
        if data is None:
            raise ValueError(f"Data for question with title slug '{self.title_slug}' is None.")
        self._data = data
    
    @property
    def params(self):
        return self._params
    
    @params.setter
    def params(self, params: dict):
        self._params = params
            
    @property
    def title_slug(self):
        return self._title_slug
    
    @title_slug.setter
    def title_slug(self, title_slug: str):
        self._title_slug = title_slug
        self._data_fetched = False
        self.params = {'titleSlug': title_slug}
        
    @property
    def data_fetched(self):
        return self._data_fetched
    
    @data_fetched.setter
    def data_fetched(self, data_fetched: bool):
        self._data_fetched = data_fetched

    @property
    def question_id(self):
        return self._data.get('questionId')

    @property
    def question_frontend_id(self):
        return self._data.get('questionFrontendId')

    @property
    def title(self):
        return self._data.get('title')

    @property
    def content(self):
        return self._data.get('content')
    
    @property
    def sample_test_case(self):
        return self._data.get('sampleTestCase')
    
    @property
    def code_snippet(self, lang='python3'):
        return next((x['code'] for x in self._data.get('codeSnippets') if x['langSlug'] == lang), None)

if __name__ == "__main__":
    details = GetQuestionDetail('two-shrtum')
    print(details.code_snippet)
    
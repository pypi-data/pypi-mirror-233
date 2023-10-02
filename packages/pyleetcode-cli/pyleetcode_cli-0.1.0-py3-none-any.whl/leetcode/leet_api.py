import requests

from leetcode.configuration import Configuration
from leetcode.graphql_query import GraphQLQuery

""" Class responsible for handling the POST requests to the 
    Leetcode GraphQL API. 
    
    config variable should be of Configuration type which contains a session_id
    for the proper work of the requests. """

class LeetAPI():
    def __init__(self, config: Configuration):
        self.config = config

    def post_query(self, query: GraphQLQuery):
        response = requests.post(url="https://leetcode.com/graphql",
                                 headers=self.config.headers,
                                 json=query.to_dict(),
                                 cookies=self.config.cookies)
        return response.json()

    def get_request(self, url):
        response = requests.get(url=url,
                                headers=self.config.headers,
                                cookies=self.config.cookies)
        return response.json()
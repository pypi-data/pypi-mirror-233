from typing import Any

""" GraphQLQuery is the main class for queries itself. Contains
    query code as well as the parameters """

class GraphQLQuery():
    types = ['query', 'variables']
    
    def __init__(self, query: str = None, variables: dict = None):
        self._query = query
        self._variables = variables

    @property
    def query(self):
        return self._query
    
    @query.setter
    def query(self, value: str):
        self._query = value
        
    @property
    def variables(self):
        return self._variables
    
    @variables.setter
    def variables(self, value: dict):
        self._variables = value
        
    def to_dict(self) -> dict:
        result = {}
        
        for item_type in self.types:
            if getattr(self, item_type) is None:
                raise ValueError(f"GraphQLQuery.{item_type} is None")
            result[item_type] = getattr(self, item_type)
            
        return result
        
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, GraphQLQuery):
            return False
        else:
            return self.query == other.query and self.variables == other.variables

    def __repr__(self) -> str:
        # String implementation for debugging purposes
        return f"GraphQLQuery(query={self.query}, variables={self.variables})"
import os
from enum import Enum, auto

import requests
from pydantic import Field

from pygraphic import GQLParameters, GQLQuery, GQLType


# Define enums
class SearchType(Enum):
    REPOSITORY = auto()
    USER = auto()


# Define query parameters (variables)
class Parameters(GQLParameters):
    query: str


# Define data models
class Repository(GQLType):
    resource_path: str


class SearchResultItemEdge(GQLType):
    node: Repository | object


class SearchResultItemConnection(GQLType):
    edges: list[SearchResultItemEdge]


# Define query model and attach variables model to it
class SearchRepositories(GQLQuery, parameters=Parameters):
    search: SearchResultItemConnection = Field(
        type=SearchType.REPOSITORY,
        query=Parameters.query,
        first=10,
    )


# Generate the GraphQL query string and instantiate variables
query_str = SearchRepositories.get_query_string()
query_params = Parameters(query="example")


# Make the request
URL = "https://api.github.com/graphql"
TOKEN = os.environ["GITHUB_TOKEN"]
response = requests.post(
    url=URL,
    json={
        "query": query_str,
        "variables": query_params.json(),
    },
    headers={
        "Authorization": f"bearer {TOKEN}",
    },
)


# Parse the response
response_json = response.json()
response_data = response_json["data"]
result = SearchRepositories.parse_obj(response_data)


# Print the results
print(f"Repositories containing '{query_params.query}':")
for edge in result.search.edges:
    print(repr(edge.node))

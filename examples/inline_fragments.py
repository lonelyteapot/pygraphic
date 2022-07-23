import os
from enum import Enum, auto

import requests
from pydantic import Field

from pygraphic import GQLQuery, GQLType


# Define enums
class SearchType(Enum):
    REPOSITORY = auto()
    # GitHub API has more enum values, but they're not necessary here


# Define data models
class Repository(GQLType):
    resource_path: str


class SearchResultItemConnection(GQLType):
    nodes: list[Repository | object]


# Define query model and attach variables model to it
class SearchRepositories(GQLQuery):
    search: SearchResultItemConnection = Field(
        type=SearchType.REPOSITORY,
        query="pydantic",
        first=10,
    )


# Generate the GraphQL query string
query_str = SearchRepositories.get_query_string()


# Make the request
URL = "https://api.github.com/graphql"
TOKEN = os.environ["GITHUB_TOKEN"]
response = requests.post(
    url=URL,
    json={
        "query": query_str,
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
print("Repositories containing 'pydantic':")
for repository in result.search.nodes:
    print(repr(repository))

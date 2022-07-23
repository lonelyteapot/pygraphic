import os

import requests
from pydantic import Field

from pygraphic import GQLQuery, GQLType


# Define data models
class PullRequest(GQLType):
    title: str


class PullRequestConnection(GQLType):
    nodes: list[PullRequest]


class Repository(GQLType):
    url: str
    pull_requests: PullRequestConnection = Field(last=10)


# Define query model
class Query(GQLQuery):
    repository: Repository = Field(owner="lonelyteapot", name="pygraphic")


# Generate the GraphQL query string and instantiate variables
query_str = Query.get_query_string(named=False)
print(query_str)


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
result = Query.parse_obj(response_data)


# Print the results
print(f"Repository url - {result.repository.url}")
print("Last 10 pull requests:")
for pull_request in result.repository.pull_requests.nodes:
    print(repr(pull_request))

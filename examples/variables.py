import os

import requests
from pydantic import Field

from pygraphic import GQLQuery, GQLType, GQLVariables


# Define the query variables
class Variables(GQLVariables):
    repo_owner: str
    repo_name: str
    pull_requests_count: int


# Define data models
class PullRequest(GQLType):
    title: str


class PullRequestConnection(GQLType):
    nodes: list[PullRequest]


class Repository(GQLType):
    url: str
    pull_requests: PullRequestConnection = Field(last=Variables.pull_requests_count)


# Define query model and attach variables to it
class PygraphicPullRequests(GQLQuery, variables=Variables):
    repository: Repository = Field(owner=Variables.repo_owner, name=Variables.repo_name)


# Generate the GraphQL query string and instantiate variables
query_str = PygraphicPullRequests.get_query_string()
variables = Variables(
    repo_owner="lonelyteapot",
    repo_name="pygraphic",
    pull_requests_count=10,
)
print(f"Query:\n{query_str}")
print(f"Variables:\n{variables}\n")


# Make the request
URL = "https://api.github.com/graphql"
TOKEN = os.environ["GITHUB_TOKEN"]
response = requests.post(
    url=URL,
    json={
        "query": query_str,
        "variables": variables.json(),
    },
    headers={
        "Authorization": f"bearer {TOKEN}",
    },
)


# Parse the response
response_json = response.json()
response_data = response_json["data"]
result = PygraphicPullRequests.parse_obj(response_data)


# Print the results
print(f"Repository url - {result.repository.url}")
print("Last 10 pull requests:")
for pull_request in result.repository.pull_requests.nodes:
    print(repr(pull_request))

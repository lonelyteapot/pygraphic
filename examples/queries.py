import os

import requests
from pydantic import HttpUrl

from pygraphic import GQLQuery, GQLType


# Define data models
class License(GQLType):
    name: str
    featured: bool
    url: HttpUrl
    # Server defines the url as a basic String, but you can use perks of pydantic
    # to make sure that the data always matches your expectations.


# Define query model
class GetAllLicenses(GQLQuery):
    licenses: list[License]


# Generate the GraphQL query string
query_str = GetAllLicenses.get_query_string()
print(query_str)


# Make the request
print("\nMaking the request...\n")
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
result = GetAllLicenses.parse_obj(response_data)


# Print the results
print(f"GitHub provides {len(result.licenses)} open-source licenses:")
for license in result.licenses:
    print()
    print(license.name)
    print(license.url)
    print("featured" if license.featured else "not featured")

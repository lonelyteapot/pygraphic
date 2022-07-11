import json
from datetime import date
from pprint import pprint

from examples.server import server_schema

import pygraphic

from .get_users_born_after import GetUsersBornAfter, Parameters


# We only want to get users born after this date
born_after = date(year=1990, month=1, day=1)


# Generate query string
gql = GetUsersBornAfter.get_query_string()
variables = Parameters(bornAfter=born_after)

# Typically you would send an HTTP Post request to a remote server.
# For simplicity, this query is processed locally.
# We dump and load json here to convert parameters from python types to strings.
response = server_schema.execute_sync(gql, json.loads(variables.json()))

# Handle errors
if response.data is None:
    raise Exception("Query failed", response.errors)

# Parse the data
result = GetUsersBornAfter.parse_obj(response.data)

# Print validated data
for user in result.users:
    print("User:", user.username)
    print("Birthday:", user.birthday)
    print("Online friends:")
    pprint(user.friends)
    print()

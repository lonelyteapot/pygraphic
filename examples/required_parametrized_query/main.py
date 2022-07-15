import json

from examples.server import server_schema

from .get_user import GetUser, Parameters


# Generate query string
gql = GetUser.get_query_string()
variables = Parameters(userId=1)

# Typically you would send an HTTP Post request to a remote server.
# For simplicity, this query is processed locally.
# We dump and load json here to convert parameters from python types to strings.
response = server_schema.execute_sync(gql, json.loads(variables.json()))

# Handle errors
if response.data is None:
    raise Exception("Query failed", response.errors)

# Parse the data
result = GetUser.parse_obj(response.data)

# Print validated data
print(result.user)

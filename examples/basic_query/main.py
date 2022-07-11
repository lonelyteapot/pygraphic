from examples.server import server_schema

from .get_all_users import GetAllUsers


# Generate query string
gql = GetAllUsers.get_query_string()

# Typically you would send an HTTP Post request to a remote server.
# For simplicity, this query is processed locally.
response = server_schema.execute_sync(gql)

# Handle errors
if response.data is None:
    raise Exception("Query failed", response.errors)

# Parse the data
result = GetAllUsers.parse_obj(response.data)

# Print validated data
for user in result.users:
    print(user.name)
    print(user.friends)

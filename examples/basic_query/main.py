import requests

from ..server import start_server
from .get_all_users import GetAllUsers


# Start a local debug server to showcase the example
start_server()


# Generate query string
gql = GetAllUsers.get_query_string()

# Make the request
url = "http://127.0.0.1:8000/graphql"
response = requests.post(url, json={"query": gql})

# Extract data from the response
json = response.json()
data = json.get("data")
if data is None:
    raise Exception("Query failed", json.get("error"))

# Parse the data
result = GetAllUsers.parse_obj(data)

# Print validated data
for user in result.users:
    print(user.name)
    print(user.friends)

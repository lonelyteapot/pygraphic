# pygraphic

Client-side GraphQL query generator based on [pydantic].

## Why?

Working with GraphQL in Python seems simple... If you're fine with dictionaries, lack of
autocompletion and unexpected errors.

Some tools allow you to generate Python code from GraphQL schemas. One of them, [turms],
even generates pydantic models from GQL documents. This approach can be problematic:
queries are written in GraphQL, not Python, so the codebase you're actually working with
is out of your control; and the main advantage of pydantic — data validation — is
missing!

## Workflow

Pygraphic is the opposite of [turms]:

1. For each individual query, you define pydantic models that you want to request,
   optionally with validators and other configuration;

2. Pygraphic converts those definitions to raw GraphQL documents *(basically strings)*;

3. Using a GraphQL or an HTTP client, you make requests with those documents and get
   back JSON responses;

4. Pydantic converts those responses to instances of the defined models and validates
   them;

5. You use the validated data, while enjoying autocompletion and type safety!

## Release Checklist

Pygraphic is in development stage. Major features might either be missing or work
incorrectly. The API may change at any time.

- [x] Basic queries
- [x] Queries with parameters
- [x] Custom scalars (not needed, comes with pydantic)
- [ ] Conversion between camelCase and snake_case
- [ ] Mutations
- [ ] Subscriptions
- [x] Tests
- [ ] Stable codebase

## Example

### Server schema
``` gql
type User {
  id: int!
  username: String!
  friends: [User!]!
}
```

### get_all_users.py

``` python
from __future__ import annotations
from pygraphic import GQLQuery, GQLType

class User(GQLType):
    id: int
    username: str
    friends: list[UserFriend]

class UserFriend(GQLType):
    id: int
    username: str

class GetAllUsers(GQLQuery):
    users: list[User]
```

### main.py

``` python
import requests
from .get_all_users import GetAllUsers

# Generate query string
gql = GetAllUsers.get_query_string()

# Make the request
url = "http://127.0.0.1/graphql"
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
    print(user.username)
    print(user.friends)
```

### Generated query string

``` gql
query GetAllUsers {
  users {
    id
    username
    friends {
      id
      username
    }
  }
}
```

See more in [/examples](https://github.com/lonelyteapot/pygraphic/tree/main/examples).

## Contribution

This project is developed on [GitHub].

If you have any general questions or need help — you're welcome in the [Discussions]
section.

If you encounter any bugs or missing features — file new [Issues], but make sure to
check the existing ones first.

If you want to solve an issue, go ahead and create a [Pull Request][Pulls]! It will be
reviewed and hopefully merged. Help is always appreciated.

## License

Copyright &copy; 2022, Dmitry Semenov. Released under the [MIT license][License].


[GitHub]: https://github.com/lonelyteapot/pygraphic
[Discussions]: https://github.com/lonelyteapot/pygraphic/discussions
[Issues]: https://github.com/lonelyteapot/pygraphic/issues
[Pulls]: https://github.com/lonelyteapot/pygraphic/pulls
[License]: https://github.com/lonelyteapot/pygraphic/blob/main/LICENSE

[pydantic]: https://pypi.org/project/pydantic/
[turms]: https://pypi.org/project/turms/

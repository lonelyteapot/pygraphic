# pygraphic
<p>
<a href="https://pypi.org/project/pygraphic" target="_blank">
    <img src="https://img.shields.io/pypi/status/pygraphic" alt="Status">
</a>
<a href="https://pypi.org/project/pygraphic" target="_blank">
    <img src="https://img.shields.io/pypi/v/pygraphic" alt="Version">
</a>
<a href="https://github.com/lonelyteapot/pygraphic/actions/workflows/test.yml?query=branch%3Amain" target="_blank">
    <img src="https://img.shields.io/github/workflow/status/lonelyteapot/pygraphic/Unit%20tests/main?label=tests" alt="Tests">
</a>
<a href="https://codecov.io/gh/lonelyteapot/pygraphic" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/lonelyteapot/pygraphic" alt="Coverage">
</a>
</p>

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

## Roadmap

Pygraphic is in development stage. Some major features are missing or might work
incorrectly. The API may change at any time.

See [ROADMAP.md][Roadmap] for the list of implemented/missing features.

## Examples

Examples are kept in the
[/examples](https://github.com/lonelyteapot/pygraphic/tree/main/examples) folder.  
Queries that they're expected to produce are stored in the
[/golden_files](https://github.com/lonelyteapot/pygraphic/tree/main/folden_files)
folder.

Most examples are based on [GitHub's GraphQL API](https://docs.github.com/en/graphql).
If you want to run them, you need to 
[generate a personal access token](https://github.com/settings/tokens) and assign it to
the environment variable called `GITHUB_TOKEN` (with VSCode, the best way to do this is
to create a [`.env` file](https://www.dotenv.org/env) in the project's root directory).

Here's the gist:

### main.py

``` python
import os
import requests
from pygraphic import GQLQuery, GQLType

# Define data models
class License(GQLType):
    id: str
    name: str
    description: str

# Define query model
class GetAllLicenses(GQLQuery):
    licenses: list[License]

# Generate the GraphQL query string
query_str = GetAllLicenses.get_query_string()

# Make the request
TOKEN = os.environ["GITHUB_TOKEN"]
response = requests.post(
    url="https://api.github.com/graphql",
    json={
        "query": query_str,
    },
    headers={
        "Authorization": f"bearer {TOKEN}",
    },
)

# Parse the response
response_data = response.json().get('data')
if response_data is None:
    print('Query failed')
result = GetAllLicenses.parse_obj(response_data)

# Print the results
for license in result.licenses:
    print(license.name)
```

### Generated query string

``` gql
query GetAllLicenses {
  licenses {
    id
    name
    description
  }
}
```

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
[Roadmap]: https://github.com/lonelyteapot/pygraphic/blob/main/ROADMAP.md

[pydantic]: https://pypi.org/project/pydantic/
[turms]: https://pypi.org/project/turms/

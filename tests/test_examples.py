from pathlib import Path


def test_arguments():
    golden_query = (
        Path("golden_files", "example_arguments.gql").read_text("utf-8").strip()
    )
    from examples.arguments import query_str, result

    assert golden_query == query_str
    assert result.repository.url
    assert result.repository.pull_requests.nodes


def test_inline_fragments():
    golden_query = (
        Path("golden_files", "example_inline_fragments.gql").read_text("utf-8").strip()
    )
    from examples.inline_fragments import Repository, query_str, result

    assert golden_query == query_str
    assert len(result.search.nodes) == 10
    assert all(type(node) is Repository for node in result.search.nodes)


def test_queries():
    golden_query = (
        Path("golden_files", "example_queries.gql").read_text("utf-8").strip()
    )
    from examples.queries import query_str

    assert golden_query == query_str


def test_variables():
    golden_query = (
        Path("golden_files", "example_variables.gql").read_text("utf-8").strip()
    )
    from examples.variables import Variables, query_str, result, variables

    golden_variables = Variables(
        repo_owner="lonelyteapot", repo_name="pygraphic", pull_requests_count=10
    )

    assert golden_query == query_str
    assert golden_variables == variables
    assert result.repository.url
    assert result.repository.pull_requests.nodes

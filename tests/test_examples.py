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

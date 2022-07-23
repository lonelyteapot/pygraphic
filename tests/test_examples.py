from pathlib import Path


def test_arguments():
    golden_query = (
        Path("golden_files", "example_arguments.gql").read_text("utf-8").strip()
    )
    from examples.arguments import query_str, result

    assert golden_query == query_str
    assert result.repository.url
    assert result.repository.pull_requests.nodes

from datetime import datetime
from uuid import UUID

import pytest
from pydantic import Field

from pygraphic import GQLQuery, GQLVariables
from pygraphic.types import register_graphql_type


def test_generation_of_query_with_custom_scalar_types():
    class Query(GQLQuery):
        uuid: UUID
        datetime: datetime

    gql = Query.get_query_string(include_name=False)
    assert gql == "query {\n  uuid\n  datetime\n}"


def test_parsing_of_query_with_custom_scalar_types():
    class Query(GQLQuery):
        uuid: UUID
        datetime: datetime

    data = {
        "uuid": "7a81e34d-ebe1-47eb-bae0-68ecc3ef174d",
        "datetime": "2001-07-01 08:30:00",
    }
    result = Query.parse_obj(data)
    assert result.uuid == UUID(hex="7a81e34d-ebe1-47eb-bae0-68ecc3ef174d")
    assert result.datetime == datetime(year=2001, month=7, day=1, hour=8, minute=30)


def test_passing_custom_scalar_types_as_field_arguments():
    uu = UUID(hex="7a81e34d-ebe1-47eb-bae0-68ecc3ef174d")
    dt = datetime(year=2001, month=7, day=1, hour=8, minute=30)

    class Query(GQLQuery):
        foo: int = Field(uuid=uu)
        bar: int = Field(datetime=dt)

    gql = Query.get_query_string(include_name=False)
    assert gql == "\n".join(
        (
            "query {",
            '  foo(uuid: "7a81e34d-ebe1-47eb-bae0-68ecc3ef174d")',
            '  bar(datetime: "2001-07-01 08:30:00")',
            "}",
        )
    )


def test_fail_of_using_custom_scalar_types_in_query_variables_without_registration():
    class Variables(GQLVariables):
        uuid: UUID
        datetime: datetime

    class Query(GQLQuery, variables=Variables):
        pass

    with pytest.raises(TypeError):
        Query.get_query_string(include_name=False)


def test_using_custom_scalar_types_in_query_variables():
    class Variables(GQLVariables):
        uuid: UUID
        datetime: datetime

    class Query(GQLQuery, variables=Variables):
        pass

    register_graphql_type("UUID", UUID)
    register_graphql_type("DateTime", datetime)

    gql = Query.get_query_string(include_name=False)
    assert gql == "query($uuid: UUID!, $datetime: DateTime!) {\n}"

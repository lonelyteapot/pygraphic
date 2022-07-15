from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import Field

from pygraphic import GQLParameters, GQLQuery, GQLType
from pygraphic.types import register_graphql_type


# Register the type so that pygraphic knows how to convert it to GraphQL
register_graphql_type("Date", date)


class Parameters(GQLParameters):
    born_after: Optional[date] = None


class User(GQLType):
    username: str
    birthday: date
    friends: list[UserFriend] = Field(online_only=True)


class UserFriend(GQLType):
    username: str
    is_online: bool


class GetUsersBornAfter(GQLQuery, parameters=Parameters):
    users: list[User] = Field(born_after=Parameters.born_after)

from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import Field

from pygraphic import GQLParameters, GQLQuery, GQLType
from pygraphic.types import register_graphql_type


# Register the type so that pygraphic knows how to convert it to GraphQL
register_graphql_type("Date", date)


class Parameters(GQLParameters):
    bornAfter: Optional[date] = None


class User(GQLType):
    username: str
    birthday: date
    friends: list[UserFriend] = Field(onlineOnly=True)


class UserFriend(GQLType):
    username: str
    isOnline: bool


class GetUsersBornAfter(GQLQuery, parameters=Parameters):
    users: list[User] = Field(bornAfter=Parameters.bornAfter)

from __future__ import annotations

from datetime import date

from pydantic import Field

from pygraphic import GQLParameters, GQLQuery, GQLType


class Parameters(GQLParameters):
    bornAfter: date


class User(GQLType):
    username: str
    birthday: date
    friends: list[UserFriend] = Field(onlineOnly=True)


class UserFriend(GQLType):
    username: str
    isOnline: bool


class GetUsersBornAfter(GQLQuery, parameters=Parameters):
    users: list[User] = Field(bornAfter=Parameters.bornAfter)

from __future__ import annotations

from pygraphic import ID, GQLQuery, GQLType


class User(GQLType):
    id: ID
    name: str
    age: int
    balance: float
    isActive: bool
    friends: list[UserFriend]


class UserFriend(GQLType):
    id: ID
    name: str


class GetAllUsers(GQLQuery):
    users: list[User]

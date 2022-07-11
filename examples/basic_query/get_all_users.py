from __future__ import annotations

from datetime import date

from pygraphic import GQLQuery, GQLType


class User(GQLType):
    id: int
    username: str
    isOnline: bool
    birthday: date
    friends: list[UserFriend]


class UserFriend(GQLType):
    id: int
    username: str


class GetAllUsers(GQLQuery):
    users: list[User]

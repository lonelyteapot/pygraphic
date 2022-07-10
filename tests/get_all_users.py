from __future__ import annotations

from uuid import UUID

from pygraphic import GQLQuery, GQLType


class User(GQLType):
    id: UUID
    username: str
    friends: list[UserFriend]


class UserFriend(GQLType):
    id: UUID
    username: str


class GetAllUsers(GQLQuery):
    users: list[User]

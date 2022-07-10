from __future__ import annotations

from uuid import UUID

from pygraphic import GQLQuery, GQLType


class User(GQLType):
    id: UUID
    name: str
    friends: list[UserFriend]


class UserFriend(GQLType):
    id: UUID
    name: str


class GetAllUsers(GQLQuery):
    users: list[User]

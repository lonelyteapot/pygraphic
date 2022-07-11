from __future__ import annotations

from pygraphic import GQLQuery, GQLType


class User(GQLType):
    id: int
    username: str


class GetAllUsers(GQLQuery):
    users: list[User]

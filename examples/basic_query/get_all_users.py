from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pygraphic import GQLQuery, GQLType


class User(GQLType):
    id: UUID
    username: str
    age: int
    balance: float
    isActive: bool
    lastSeen: datetime
    friends: list[UserFriend]


class UserFriend(GQLType):
    id: UUID
    username: str


class GetAllUsers(GQLQuery):
    users: list[User]

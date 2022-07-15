from __future__ import annotations

from pydantic import Field

from pygraphic import GQLParameters, GQLQuery, GQLType


class Parameters(GQLParameters):
    user_id: int


class User(GQLType):
    id: int
    username: str


class GetUser(GQLQuery, parameters=Parameters):
    user: User = Field(id=Parameters.user_id)

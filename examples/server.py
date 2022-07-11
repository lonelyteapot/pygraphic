from __future__ import annotations

from datetime import datetime, timedelta
from random import randint, randrange
from uuid import UUID, uuid4

import strawberry
from faker import Faker


@strawberry.type
class User:
    id: UUID
    name: str
    age: int
    balance: float
    is_active: bool
    last_seen: datetime
    friends: list[User]


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> list[User]:
        return _users


_fake = Faker()
_users = [
    User(
        id=uuid4(),
        name=_fake.name(),
        age=randint(14, 80),
        balance=randint(0, 1000) / 100,
        is_active=bool(randint(0, 1)),
        last_seen=datetime.now() - timedelta(minutes=randint(1, 200)),
        friends=list(),
    )
    for _ in range(randrange(5, 10))
]

for next_i, user in enumerate(_users, 1):
    for possible_friend in _users[next_i:]:
        if randint(0, 1):
            user.friends.append(possible_friend)
            possible_friend.friends.append(user)


server_schema = strawberry.Schema(query=Query)

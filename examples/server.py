from __future__ import annotations

from datetime import date, datetime
from random import choices, randint, randrange
from string import ascii_lowercase

import strawberry


@strawberry.type
class User:
    id: int
    username: str
    is_online: bool
    birthday: date
    friends: list[User]


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> list[User]:
        return _users


_users = [
    User(
        id=id,
        username="".join(choices(ascii_lowercase, k=randint(8, 16))),
        is_online=bool(randint(0, 1)),
        birthday=date.fromtimestamp(randrange(0, int(datetime.now().timestamp()))),
        friends=list(),
    )
    for id in range(randrange(5, 10))
]

for next_i, user in enumerate(_users, 1):
    for possible_friend in _users[next_i:]:
        if randint(0, 1):
            user.friends.append(possible_friend)
            possible_friend.friends.append(user)


server_schema = strawberry.Schema(query=Query)

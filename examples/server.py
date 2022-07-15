from __future__ import annotations

from datetime import date, datetime
from random import choices, randint, randrange
from string import ascii_lowercase
from typing import Optional

import strawberry


@strawberry.type
class User:
    id: int
    username: str
    is_online: bool
    birthday: date
    _friends: strawberry.Private[list[User]]

    @strawberry.field
    def friends(self, online_only: bool = False) -> list[User]:
        if online_only:
            return [friend for friend in self._friends if friend.is_online]
        return self._friends


@strawberry.type
class Query:
    @strawberry.field
    def users(self, born_after: Optional[date] = None) -> list[User]:
        if born_after is not None:
            return [user for user in _users if user.birthday > born_after]
        return _users

    @strawberry.field
    def user(self, id: int) -> User:
        return next(filter(lambda user: user.id == id, _users))


_users = [
    User(
        id=id,
        username="".join(choices(ascii_lowercase, k=randint(8, 16))),
        is_online=bool(randint(0, 1)),
        birthday=date.fromtimestamp(randrange(0, int(datetime.now().timestamp()))),
        _friends=list(),
    )
    for id in range(randrange(5, 10))
]

for next_i, user in enumerate(_users, 1):
    for possible_friend in _users[next_i:]:
        if randint(0, 1):
            user._friends.append(possible_friend)
            possible_friend._friends.append(user)


server_schema = strawberry.Schema(query=Query)

from typing import Iterator


def first_only() -> Iterator[bool]:
    yield True
    while True:
        yield False

from typing import NewType


ID = NewType("ID", str)

KNOWN_SCALARS = (int, float, str, bool, ID)

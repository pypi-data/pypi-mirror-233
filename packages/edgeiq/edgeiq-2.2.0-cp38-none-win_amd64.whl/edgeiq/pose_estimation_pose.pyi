from _typeshed import Incomplete
from typing import List, NamedTuple, Tuple

class Coord(NamedTuple):
    x: Incomplete
    y: Incomplete

class Pose:
    def __init__(self, key_points: List[Tuple[int, int]], score: float) -> None: ...
    def __eq__(self, other): ...
    @property
    def key_points(self) -> dict: ...
    @property
    def score(self) -> float: ...

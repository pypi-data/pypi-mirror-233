from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, TypeVar, Generic, Optional

T = TypeVar("T")


@dataclass
class Node(Generic[T]):
    """A Node can have a maximum of one parent and zero to N number of children."""

    value: T
    parent: Optional[Node]
    children: List[Node] = field(default_factory=list)

    _level: int = field(init=False, default=0)

    def __post_init__(self):
        if self.parent:
            self._level = self.parent._level + 1

    def __lt__(self, other: Node) -> bool:
        return self.value > other.value

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, int) -> None:
        raise NotImplementedError("Not expected to be set externally.")


class File(Node):
    def __init__(self, name: str, parent: Node):
        super().__init__(name, parent)


class Folder(Node):
    def __init__(
        self, name, parent: Optional[Node], children: Optional[List[Node]] = None
    ):
        if children is None:
            children = []
        super().__init__(name, parent, children)

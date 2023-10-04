from collections import defaultdict
from dataclasses import field, dataclass
from enum import Enum, auto

"""A Renderer is a representation of how a fs should be printed."""


@dataclass
class RenderTag:
    open: str = field(default="")
    close: str = field(default="")


class RenderTagEnum(Enum):
    DOC = auto()
    ROOT = auto()
    FILE = auto()
    FOLDER = auto()


class Renderer:
    """A Renderer provides special instructions for how a fs is displayed."""

    def __init__(self):
        self._tags = defaultdict(RenderTag)

    def register(self, key: RenderTagEnum, tags: RenderTag):
        self._tags[key] = tags

    def tags(self, key: RenderTagEnum) -> RenderTag:
        return self._tags[key]


defaultRenderer = Renderer()
defaultRenderer.register(RenderTagEnum.DOC, RenderTag("", "\n"))
defaultRenderer.register(RenderTagEnum.ROOT, RenderTag("", ":\\"))
defaultRenderer.register(RenderTagEnum.FOLDER, RenderTag("", "\\"))

markdownRenderer = Renderer()
markdownRenderer.register(
    RenderTagEnum.DOC, RenderTag('<pre style="line-height:17px\n">', "</pre>")
)
defaultRenderer.register(RenderTagEnum.ROOT, RenderTag("", ":\\"))
defaultRenderer.register(RenderTagEnum.FOLDER, RenderTag("", "\\"))
markdownRenderer.register(
    RenderTagEnum.FILE, RenderTag('<span style="color:gray">', "</span>")
)


emojiRenderer = Renderer()
emojiRenderer.register(RenderTagEnum.DOC, RenderTag("", "\n"))
emojiRenderer.register(RenderTagEnum.ROOT, RenderTag("🏡", ":"))
emojiRenderer.register(RenderTagEnum.FILE, RenderTag("📄", ""))
emojiRenderer.register(RenderTagEnum.FOLDER, RenderTag("📁", ""))

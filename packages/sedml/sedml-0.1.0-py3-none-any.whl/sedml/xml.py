from typing import TYPE_CHECKING

try:
    from lxml.etree import _Comment, fromstring  # type: ignore
    from lxml.etree import _Element as Element

    def is_comment(x: Element):  # type: ignore
        return isinstance(x, _Comment)

except ImportError:
    from xml.etree.ElementTree import Comment as _Comment
    from xml.etree.ElementTree import Element, fromstring

    def is_comment(x: Element):
        return x.tag is _Comment


__all__ = [
    "fromstring",
    "Element",
    "is_comment",
]


if TYPE_CHECKING:

    def fromstring(text: str | bytes, /) -> Element:  # noqa
        ...

import io
from typing import Any, Callable, Sequence

import rich
from pydantic import BeforeValidator, PlainSerializer
from pydantic_xml import BaseXmlModel
from typing_extensions import Annotated

from .xml import Element


class _BaseSEDML(BaseXmlModel):
    def __repr__(self) -> str:
        sio = io.StringIO()
        rich.print(self, file=sio)
        return sio.getvalue()

    def __rich_repr__(self):
        for a, v in self.__repr_args__():
            if v is None or isinstance(v, Sequence) and len(v) == 0:
                continue
            elif a is None:
                yield v
            else:
                yield a, v

    def to_xml(
        self,
        *,
        skip_empty: bool = True,
        **kwargs,
    ) -> str | bytes:
        return super().to_xml(skip_empty=skip_empty, **kwargs)

    def to_xml_tree(self, *, skip_empty: bool = True) -> Element:
        return super().to_xml_tree(skip_empty=skip_empty)


def try_types(*types: Callable[[str], Any]):
    def parser(x):
        x = x.strip()
        for f in types:
            try:
                return f(x)
            except Exception:
                pass

    return parser


def bool_parser(x):
    match x:
        case "1" | "true":
            return True
        case "0" | "false":
            return False
        case _:
            raise ValueError(x)


BOOL = Annotated[
    bool,
    BeforeValidator(bool_parser),
    PlainSerializer(lambda x: "true" if x else "false"),
]
INT = Annotated[int, BeforeValidator(try_types(int))]
FLOAT = Annotated[float, BeforeValidator(try_types(float))]
FLOAT_BOOL_STR = Annotated[
    float | bool | str, BeforeValidator(try_types(float, bool_parser, str))
]


# letter ::= ’a’..’z’,’A’..’Z’ digit ::= ’0’..’9’ idChar ::= letter | digit | ’ ’ SId ::= ( letter | ’ ’ ) idChar*

from __future__ import annotations

from os import PathLike

from . import l1v1, l1v2, l1v3, l1v4, xml

SEDML = l1v1.SEDML | l1v2.SEDML | l1v3.SEDML | l1v4.SEDML

readers: dict[tuple[str, str], type[SEDML]] = {
    ("1", "1"): l1v1.SEDML,
    ("1", "2"): l1v2.SEDML,
    ("1", "3"): l1v3.SEDML,
    ("1", "4"): l1v4.SEDML,
}


def load(file: PathLike):
    with open(file, "rb") as f:
        return loads(f.read())


def loads(text: str | bytes):
    xml_tree = xml.fromstring(text)
    level = xml_tree.attrib["level"]
    version = xml_tree.attrib["version"]
    try:
        reader = readers[level, version]
    except KeyError:
        raise TypeError(
            f"reader for SED-ML level {level} version {version} not implemented"
        )
    else:
        return reader.from_xml_tree(xml_tree)


def dump(
    sedml: SEDML,
    file: PathLike,
    *,
    encoding="UTF-8",
    xml_declaration: bool = True,
    pretty_print: bool = True,
) -> None:
    bytes = dumps(
        sedml,
        encoding=encoding,
        xml_declaration=xml_declaration,
        pretty_print=pretty_print,
    )
    with open(file, "wb") as f:
        f.write(bytes)


def dumps(
    sedml: SEDML,
    *,
    encoding="UTF-8",
    xml_declaration: bool = True,
    pretty_print: bool = True,
) -> bytes:
    return sedml.to_xml(
        encoding=encoding,
        xml_declaration=xml_declaration,
        pretty_print=pretty_print,
    )

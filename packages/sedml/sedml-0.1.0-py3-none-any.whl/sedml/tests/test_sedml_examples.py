from pathlib import Path

from pytest import mark

from .common import load_and_compare

root = Path("src/sedml/tests/sed-ml/specification")


def yield_sedml_files():
    for file in root.rglob("*.xml"):
        if "<sedML" in file.read_text():
            yield str(file.relative_to(root))


@mark.parametrize("file", sorted(yield_sedml_files()))
def test_roundtrip(file: str):
    path = root / file
    load_and_compare(path.read_bytes())

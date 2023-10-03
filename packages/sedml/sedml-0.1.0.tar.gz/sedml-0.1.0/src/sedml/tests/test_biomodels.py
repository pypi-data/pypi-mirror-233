from typing import Iterator
from zipfile import Path

import biomodels
from biomodels.common import cache_path
from pytest import mark

from .common import load_and_compare


def yield_sedml(f) -> Iterator[Path]:
    omex = biomodels.get_omex(f)
    for content in omex:
        if str(content.location).endswith(".sedml"):
            yield content.path


def has_sedml(f) -> bool:
    for _ in yield_sedml(f):
        return True
    return False


cache = cache_path / "omex"
if cache.exists():
    files = sorted(filter(has_sedml, (p.stem for p in cache.iterdir())))
else:
    # Download 10 with the smallest file size
    # 105 kB in total
    files = [
        "BIOMD0000000850",
        "BIOMD0000000785",
        "BIOMD0000000799",
        "BIOMD0000000922",
        "BIOMD0000000815",
        "BIOMD0000000936",
        "BIOMD0000000787",
        "BIOMD0000000893",
        "BIOMD0000001045",
        "BIOMD0000000935",
    ]


@mark.parametrize("file", files)
def test_roundtrip(file):
    for p in yield_sedml(file):
        load_and_compare(p.read_bytes())

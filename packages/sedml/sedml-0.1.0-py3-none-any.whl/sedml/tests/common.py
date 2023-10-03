from .. import dumps, loads
from ..common import bool_parser, try_types
from ..xml import Element, fromstring, is_comment

float_bool_str = try_types(float, bool_parser, str)

deprecated: dict[str, set[str]] = {
    "{http://sed-ml.org/sed-ml/level1/version4}curve": {"logX", "logY"},
}


def compare_xml(x: Element, y: Element):
    """Compare two XML trees."""
    assert x.tag == y.tag
    x_keys = set(xi for xi in x.attrib.keys())
    y_keys = set(yi for yi in y.attrib.keys())
    diff: set[str] = set.symmetric_difference(x_keys, y_keys)
    # TODO: remove this hack to exclude some keys with extra namespaces.
    diff = {x for x in diff if not x.startswith("{")}
    # Deprecated elements are ignored during parsing
    # and not recreated after the round trip.
    # We remove those keys.
    deprecated_keys = deprecated.get(x.tag, set())
    diff = diff.difference(deprecated_keys)
    assert len(diff) == 0, diff

    for k, xv in x.attrib.items():
        if "{" in k or k in deprecated_keys:
            continue
        yv = y.attrib[k]
        assert float_bool_str(xv) == float_bool_str(yv), (k, xv, yv)

    x_elements: list[Element] = [xi for xi in x if not is_comment(xi)]

    def get_tag(x):
        return x.tag

    x_elements = sorted(x_elements, key=get_tag)
    y_elements = sorted(y, key=get_tag)
    assert all(map(compare_xml, x_elements, y_elements))
    return True


def load_and_compare(b: bytes):
    direct = fromstring(b)
    round_trip = fromstring(dumps(loads(b)))
    compare_xml(direct, round_trip)

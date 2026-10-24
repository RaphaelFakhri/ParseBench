"""Sidecars carrying data_schema, layout rules and extract_field rules together."""

import json
from pathlib import Path

from parse_bench.test_cases.loader import load_test_cases
from parse_bench.test_cases.schema import ExtractTestCase


def test_parse_hint_keeps_mixed_layout_and_extract_field_sidecar_loadable(tmp_path: Path) -> None:
    """With the PARSE hint, a sidecar that also has extract_field rules must stay an
    ExtractTestCase; routing it to LayoutDetectionTestCase raised
    ``Unknown parse rule type: extract_field`` and aborted the whole evaluation."""
    group_dir = tmp_path / "forms"
    group_dir.mkdir()
    (group_dir / "doc.pdf").write_bytes(b"%PDF-1.4\n")
    test_json = {
        "data_schema": {"type": "object", "properties": {"name": {"type": "string"}}},
        "expected_output": {"name": "Ada"},
        "test_rules": [
            {"type": "layout", "id": "l1", "page": 1, "bbox": [0.1, 0.1, 0.5, 0.05], "canonical_class": "Text"},
            {
                "type": "extract_field",
                "field_path": "name",
                "expected_value": "Ada",
                "bboxes": [{"page": 1, "bbox": [0.1, 0.1, 0.2, 0.05]}],
            },
        ],
    }
    (group_dir / "doc.test.json").write_text(json.dumps(test_json))

    cases = load_test_cases(tmp_path, product_type="parse")

    assert len(cases) == 1
    assert isinstance(cases[0], ExtractTestCase)
    assert len(cases[0].get_extract_field_rules()) == 1

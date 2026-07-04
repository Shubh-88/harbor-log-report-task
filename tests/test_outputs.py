"""Verifier for dynamo/log-report.

Each test maps 1-to-1 to a numbered success criterion in instruction.md.
A no-op agent (file absent or wrong values) must score 0; the oracle must score 1.
"""

import json
from pathlib import Path

REPORT = Path("/app/report.json")


def _load():
    assert REPORT.exists(), "/app/report.json was not created"
    with REPORT.open() as f:
        return json.load(f)


def test_total_requests():
    """Criterion 1: total_requests equals 6 (one entry per log line)."""
    data = _load()
    assert "total_requests" in data, "key 'total_requests' missing from report"
    assert data["total_requests"] == 6, (
        f"expected total_requests=6, got {data['total_requests']}"
    )


def test_unique_ips():
    """Criterion 2: unique_ips equals 3 (192.168.0.1, 192.168.0.2, 10.0.0.5)."""
    data = _load()
    assert "unique_ips" in data, "key 'unique_ips' missing from report"
    assert data["unique_ips"] == 3, (
        f"expected unique_ips=3, got {data['unique_ips']}"
    )


def test_top_path():
    """Criterion 3: top_path is '/index.html' (requested 3 times)."""
    data = _load()
    assert "top_path" in data, "key 'top_path' missing from report"
    assert data["top_path"] == "/index.html", (
        f"expected top_path='/index.html', got {data['top_path']!r}"
    )

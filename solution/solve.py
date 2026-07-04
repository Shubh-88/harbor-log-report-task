#!/usr/bin/env python3
"""Oracle solution for dynamo/log-report."""

import json
import re
from collections import Counter
from pathlib import Path

LOG = Path("/app/access.log")
REPORT = Path("/app/report.json")

lines = LOG.read_text().splitlines()
lines = [l for l in lines if l.strip()]

total_requests = len(lines)
ips = set()
paths = []

for line in lines:
    parts = line.split()
    if parts:
        ips.add(parts[0])
    # path is inside "METHOD /path HTTP/x.x"
    m = re.search(r'"[A-Z]+ (/\S*) HTTP/', line)
    if m:
        paths.append(m.group(1))

path_counts = Counter(paths)
top_path = path_counts.most_common(1)[0][0] if path_counts else ""

report = {
    "total_requests": total_requests,
    "unique_ips": len(ips),
    "top_path": top_path,
}

REPORT.write_text(json.dumps(report, indent=2) + "\n")
print(f"Wrote {REPORT}: {report}")

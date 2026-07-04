# harbor-log-report

A Harbor TB2 evaluation task: parse an Apache-style access log into a JSON summary report.

---

## Task overview

The agent is given an Apache Combined Log Format file at `/app/access.log` (6 lines, 3 unique IPs) and must produce `/app/report.json` containing exactly three keys:

| Key | Expected value |
|---|---|
| `total_requests` | `6` |
| `unique_ips` | `3` |
| `top_path` | `"/index.html"` |

---

## Directory structure

```
log-report/
├── task.toml                  # Harbor task metadata & config
├── instruction.md             # Prompt shown to the agent
├── environment/
│   ├── Dockerfile             # Agent container (python:3.13-slim-bookworm, pinned digest)
│   └── access.log             # Input data — 6 lines, 3 IPs
├── solution/
│   ├── solve.sh               # Oracle entry-point (called by harbor -a oracle)
│   └── solve.py               # Reference solution
└── tests/
    ├── test.sh                # Verifier entry-point — runs pytest, writes reward.txt + ctrf.json
    └── test_outputs.py        # Three pytest tests, one per success criterion
```

> `environment/solution_hint.py` does **not** exist — it was removed to prevent leaking the solution into the agent image.

---

## Running with Harbor

```bash
# Build the task image
harbor build -p log-report

# Oracle run — expect reward.txt = 1
harbor run -p log-report -a oracle

# No-op agent run — expect reward.txt = 0
harbor run -p log-report --agent nop
```

---

## Running locally (without Harbor/Docker)

### Prerequisites

```bash
pip install pytest==8.4.1 pytest-json-ctrf==0.3.5
```

Or install from the requirements file:

```bash
pip install -r requirements.txt
```

### Simulate oracle run

```bash
# 1. Copy access.log to /app (or adjust path in solve.py)
sudo mkdir -p /app && sudo chmod 777 /app
cp environment/access.log /app/access.log

# 2. Run oracle
python3 solution/solve.py

# 3. Run verifier
mkdir -p /logs/verifier
pytest tests/test_outputs.py -rA --ctrf /logs/verifier/ctrf.json -v
cat /logs/verifier/reward.txt   # → 1
```

### Simulate nop agent run (no report.json written)

```bash
rm -f /app/report.json
pytest tests/test_outputs.py -rA -v
# All 3 tests fail → reward = 0
```

---

## Verifier outputs

### `-a oracle` (reward = 1)

```
reward.txt: 1

passed: 3  failed: 0  total: 3
  [PASSED] test_outputs.py::test_total_requests
  [PASSED] test_outputs.py::test_unique_ips
  [PASSED] test_outputs.py::test_top_path
```

### `--agent nop` (reward = 0)

```
reward.txt: 0

passed: 0  failed: 3  total: 3
  [FAILED] test_outputs.py::test_total_requests  — AssertionError: /app/report.json was not created
  [FAILED] test_outputs.py::test_unique_ips      — AssertionError: /app/report.json was not created
  [FAILED] test_outputs.py::test_top_path        — AssertionError: /app/report.json was not created
```

### Bugged solve.sh (reward = 0)

Bugged snippet introduced for proof:

```bash
#!/bin/bash
set -euo pipefail
# BUG: hardcoded wrong values instead of computing from the log
python3 -c "
import json
report = {'total_requests': 99, 'unique_ips': 1, 'top_path': '/wrong.html'}
open('/app/report.json', 'w').write(json.dumps(report))
"
```

Verifier output:

```
reward.txt: 0

passed: 0  failed: 3  total: 3
  [FAILED] test_total_requests — AssertionError: expected total_requests=6, got 99
  [FAILED] test_unique_ips     — AssertionError: expected unique_ips=3, got 1
  [FAILED] test_top_path       — AssertionError: expected top_path='/index.html', got '/wrong.html'
```

---

## Fixes applied

| File | What was fixed |
|---|---|
| `task.toml` | `artifacts` changed from string `"/app/out.json"` → array `["/app/report.json"]` |
| `environment/Dockerfile` | Pinned base image digest; removed `COPY solution_hint.py` |
| `environment/solution_hint.py` | **Deleted** (leaked solution — must not be in agent image) |
| `tests/test.sh` | Output path fixed from `/app/reward.txt` → `/logs/verifier/`; added `--ctrf` flag |
| `tests/test_outputs.py` | Tests now assert actual computed values, not just file existence |
| `instruction.md` | Added output path, exact key names, numbered success criteria |
=======
# harbor-log-report-task
Handshake AI log reports task

# Harbor Log Report Task

## Overview

This repository contains a Harbor (Terminal-Bench 2) task that parses an Apache access log and generates a JSON summary report.

The generated report contains:

- total_requests
- unique_ips
- top_path

## Project Structure

```
environment/
solution/
tests/
task.toml
instruction.md
```

## Requirements

- Docker
- Harbor
- Python 3.11+

## Running

Build:

```bash
harbor build -p .
```

Run Oracle:

```bash
harbor run -p . --agent oracle
```

Run NOP:

```bash
harbor run -p . --agent nop
```

## Expected Behaviour

- Oracle should receive reward **1.0**
- NOP should receive reward **< 1.0**

## Files

- `task.toml` — Harbor configuration
- `instruction.md` — Task instructions
- `environment/` — Docker image and input data
- `solution/` — Reference solution
- `tests/` — Verification tests
>>>>>>> 80fa38ef0f33a89ea9f97a5ac047a92257e85d57

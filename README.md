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

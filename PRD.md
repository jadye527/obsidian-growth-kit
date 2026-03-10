# Obsidian Growth Kit — Code Improvements

## Overview
Improve code quality, add tests, and set up CI for the Obsidian Growth Kit — a set of CLI tools for autonomous X/Twitter growth.

## Requirements

### Code Quality
- [x] Add `--help` flag with usage examples to `tools/xpost` (argparse or manual)
- [x] Add `--help` flag with usage examples to `tools/xqueue`
- [x] Add `--help` flag with usage examples to `tools/xanalytics`
- [x] Add `--help` flag with usage examples to `tools/xscout`
- [x] Add `--help` flag with usage examples to `tools/xgrowth`
- [x] Add proper error handling to `tools/xpost` — catch network errors, missing credentials, bad tweet IDs
- [x] Add proper error handling to `tools/xqueue` — catch file read/write errors, empty queue
- [x] Add input validation to all tools — handle missing args gracefully with helpful messages
- [x] Fix any remaining hardcoded paths (replace with `os.path.expanduser("~")` or `$HOME`)

### Testing
- [x] Create `tests/test_xqueue.py` with pytest tests for add, list, flush, count, cooldown logic
- [x] Create `tests/test_xgrowth.py` with pytest tests for categorization and strategy logging
- [x] Create `tests/test_xscout.py` with pytest tests for tweet parsing, scoring, dedup
- [x] Create `tests/conftest.py` with shared fixtures (temp dirs, mock data)

### CI/CD
- [x] Create `.github/workflows/test.yml` — run pytest on every push and PR
- [x] Create `.github/workflows/lint.yml` — run ruff or flake8 on every push and PR
- [x] Create `pyproject.toml` with project metadata and dependencies

### Documentation
- [x] Create `docs/API-REFERENCE.md` documenting all commands for all 6 tools
- [x] Add docstrings to all public functions in the Python tools

## Tech Stack
- Python 3.10+
- pytest for testing
- GitHub Actions for CI
- ruff for linting

## Constraints
- Do not add any API keys or credentials to the repo
- All paths must use `~` or env vars, never hardcoded
- Tools must work standalone (no server needed)
- Keep dependencies minimal (tweepy, asciinema only)

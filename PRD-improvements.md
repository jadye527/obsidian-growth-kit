# Obsidian Growth Kit — Improvement PRD

## Overview
Continuous improvement tasks for the Obsidian Growth Kit product.
Ralph should work through these autonomously, creating PRs for review.

## Task List

### Priority 1: Code Quality
1. Add proper error handling to all CLI tools (xpost, xqueue, xanalytics, xscout, xgrowth) — graceful failures with helpful error messages
2. Add `--help` flag to every tool with usage examples
3. Add input validation — handle missing args, bad tweet IDs, network errors
4. Fix any hardcoded paths remaining (should all use `~` or env vars)
5. Add type hints to all Python functions

### Priority 2: Testing
6. Create `tests/` directory with pytest test files
7. Unit tests for xqueue (add, list, flush, count, cooldown logic)
8. Unit tests for xanalytics (snapshot parsing, comparison logic)
9. Unit tests for xscout (tweet parsing, scoring, dedup)
10. Unit tests for xgrowth (categorization, strategy logging)
11. Integration test: full workflow (queue → post → track)

### Priority 3: Features
12. Add `xpost bookmark <id>` and `xpost unbookmark <id>` commands
13. Add `xqueue schedule <time> "text"` — schedule for specific time
14. Add `xanalytics export --csv` — export metrics to CSV
15. Add `xscout watch <query>` — continuous monitoring mode
16. Add `xgrowth ab-test` — A/B test tracking between post formats
17. Add `xrecord gif <name>` — convert recordings to GIF using ffmpeg

### Priority 4: Documentation
18. Add docstrings to all functions
19. Create `docs/API-REFERENCE.md` with all commands documented
20. Create `docs/ARCHITECTURE.md` explaining how tools connect
21. Add inline comments for complex logic

### Priority 5: CI/CD
22. Create `.github/workflows/test.yml` — run tests on PR
23. Create `.github/workflows/lint.yml` — run flake8/ruff on PR
24. Add `setup.py` or `pyproject.toml` for pip installability

## Acceptance Criteria
- All tests pass
- No hardcoded paths or credentials
- Every tool has `--help`
- CI pipeline runs on every PR
- Code follows PEP 8

# Agentic Dataset Update Guide

This repository uses an agentic GitHub Actions workflow to keep dataset files current.

## What the workflow does

1. Reads repository context:
   - `README.md`
   - `datapackage.json`
   - `scripts/`
2. Determines the native update command and source endpoints.
3. Compares local freshness (latest date/year in `data/`) vs upstream freshness.
4. If stale, runs the native update command.
5. Re-checks freshness and prints evidence.
6. Opens a PR if files changed.

## Freshness rule

- Up-to-date means local max date/year equals source max date/year.
- If source is newer, the workflow must update and re-validate.

## Required tooling in CI

- `duckdb` for CSV/JSON max checks
- `pandas` for wrangling and comparisons
- `requests` for source fetches
- `xlrd`/`openpyxl` for spreadsheet sources
- `dataflows`, `datapackage`, `goodtables` for dataset pipelines/validation

## OpenCode execution

The workflow invokes:

```bash
opencode run --model <provider/model> -f .github/AGENTIC_DATASET_UPDATE_GUIDE.md "<instructions>"
```

## Manual trigger support

In GitHub Actions UI, use **Run workflow** and optionally set:

- `model` (e.g. `openai/gpt-5.3-codex`)
- `dry_run` (`true` to only check freshness)

## API key options

Configure one or more provider secrets in repository settings:

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GOOGLE_API_KEY`
- `ZEN_AI_API_KEY` (optional; included to support Zen provider setups)

If you use Zen models, set a matching model string in workflow input/variable (for example, a Zen provider model identifier supported by your OpenCode setup).

## Safety constraints

- Do not push directly to `main`.
- Let the workflow create a pull request.
- Keep schema stable unless source requires changes.

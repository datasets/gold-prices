#!/usr/bin/env bash
set -euo pipefail

MODEL="${OPENCODE_MODEL:-openai/gpt-5.3-codex}"
DRY_RUN="${OPENCODE_DRY_RUN:-false}"

GUIDE_FILE=".github/AGENTIC_DATASET_UPDATE_GUIDE.md"

if [[ ! -f "${GUIDE_FILE}" ]]; then
  echo "Error: missing required guide file: ${GUIDE_FILE}" >&2
  pwd >&2
  ls -la >&2
  exit 1
fi

PROMPT_FILE="$(mktemp)"
cat >"${PROMPT_FILE}" <<'EOF'
Use the attached repository guide first, then execute the workflow tasks.

Tasks:
1) Discover source endpoints, native update commands, and output files by reading README.md, datapackage.json, and scripts/.
2) Compute local freshness maxima from current data files.
3) Compute upstream freshness maxima from source endpoints.
4) If up to date, print concise evidence and exit successfully without file changes.
5) If stale and DRY_RUN=false, run native update command(s), then re-validate maxima.
6) Keep schema stable unless source changed.
7) Print concise report with before/after maxima and changed files.

Constraints:
- Prefer existing repo scripts over new pipelines.
- Do not commit or push.
EOF

if [[ "${DRY_RUN}" == "true" ]]; then
  echo "Running in dry-run mode (freshness check only)."
  EXTRA_NOTE="DRY_RUN is true. Do not run update commands."
else
  EXTRA_NOTE="DRY_RUN is false. Run update commands only if stale."
fi

echo "Running OpenCode with model: ${MODEL}"
opencode run \
  --model "${MODEL}" \
  -f "${GUIDE_FILE}" \
  "$(cat "${PROMPT_FILE}") ${EXTRA_NOTE}"

rm -f "${PROMPT_FILE}"

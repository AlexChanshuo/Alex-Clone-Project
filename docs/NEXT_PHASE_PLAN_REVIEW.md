# Next Phase Plan Review

This document records the plan review before building the next phase after
fetch plans and checkpoints.

## Current State Reviewed

Implemented and verified:

- Telegram-style command parser.
- Local approved LINE group watchlist with tags.
- Personal LINE fetch plans.
- Per-group fetch checkpoints.
- Manual JSONL ingest into `alex-mind`.
- Daily report generator.
- Reply draft policy gate.
- Bilingual agent and layman guides.

Not implemented yet:

- Reading live LINE UI.
- Turning Computer Use screen captures into normalized `LineEvent` records.
- A command workflow that turns `掃 AI 群` into fetch targets and ingestion
  instructions.
- A combined capture ingest flow that writes raw data, updates checkpoints, and
  optionally generates a report.

## Plan Cycle 1

Build the LINE capture normalization layer.

Goal:

Computer Use or a human can provide one capture JSON file representing messages
seen in a LINE group. Alex Clone converts that capture into normalized
`LineEvent` JSONL.

Deliverables:

- `line_capture.py`
- Capture JSON schema.
- Group title validation using display name and aliases.
- Deterministic message IDs/fingerprints.
- CLI command: `normalize-capture`.
- Tests for title validation and missing timestamps.

Review:

This is the right first build because it does not depend on fragile UI
automation. It creates the contract the UI reader must satisfy.

## Plan Cycle 2

Build the command-to-fetch and capture-ingest workflow.

Goal:

Telegram-style commands can be translated into target groups and fetch plans,
then a captured JSON file can be ingested with checkpoint updates and optional
report generation.

Deliverables:

- CLI command: `command-plan`.
- CLI command: `ingest-capture`.
- Combined flow:
  - validate group,
  - normalize capture,
  - filter already-seen events,
  - write raw events to `alex-mind`,
  - update checkpoint,
  - optionally write report/digest.
- Docs in `RUNTIME_CLI.md`, `AGENT_GUIDE_EN_ZH.md`, and
  `LAYMAN_GUIDE_EN_ZH.md`.

Review:

This keeps the next live Computer Use phase small: the UI reader only needs to
produce capture JSON. The rest of the pipeline can already be tested and reused.

## Safety Decisions

- Do not auto-send in this phase.
- Do not commit real captures.
- Do not commit `.env`, `config/groups.json`, or `.alex-clone-state/`.
- Require group title validation before ingesting a capture.
- Mark missing timestamps with lower confidence.

## Build Cycle Review

### Cycle 1 Result

Implemented:

- `line_capture.py`
- `normalize-capture`
- capture fixture
- capture tests

Review:

The capture JSON contract works and validates group titles before conversion.
Messages without explicit timestamps are allowed, but their confidence is
lowered and metadata records `timestamp_inferred: true`.

### Cycle 2 Result

Implemented:

- `command-plan`
- `ingest-capture`
- command workflow tests
- temp-vault-safe testing pattern

Review:

The runtime can now go from Telegram wording to target fetch plans, then from a
Computer Use capture JSON to raw vault writes, checkpoint updates, and report
output. The real remaining blocker is the UI reader that produces capture JSON
from LINE.

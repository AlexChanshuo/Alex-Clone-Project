# Runtime CLI

The current V1 implementation is a dependency-free Python scaffold. It does not
yet click LINE by itself; it prepares safe personal LINE execution plans and
handles local ingestion, reports, vault writes, and policy checks.

Run commands from the repo root:

```bash
PYTHONPATH=src python3 -m alex_clone.cli status
```

## Commands

### `groups`

Lists the local approved/follow-up group watchlist. Filter by tag when needed.

```bash
PYTHONPATH=src python3 -m alex_clone.cli groups
PYTHONPATH=src python3 -m alex_clone.cli groups --tag BNI
PYTHONPATH=src python3 -m alex_clone.cli groups --tag AI
```

### `status`

Shows loaded repo path, `alex-mind` path, group config, and policy config.

```bash
PYTHONPATH=src python3 -m alex_clone.cli status
```

### `ingest-manual`

Appends normalized LINE event JSONL into:

```text
alex-mind/raw/inbox/line/YYYY-MM-DD/<group-slug>.jsonl
```

```bash
PYTHONPATH=src python3 -m alex_clone.cli ingest-manual tests/fixtures/line_events.jsonl
```

### `daily-report`

Generates a Markdown report from a JSONL capture. Add `--save` to write it into
`alex-mind`.

```bash
PYTHONPATH=src python3 -m alex_clone.cli daily-report tests/fixtures/line_events.jsonl --date 2026-05-20
PYTHONPATH=src python3 -m alex_clone.cli daily-report tests/fixtures/line_events.jsonl --date 2026-05-20 --save
```

### `draft-reply`

Creates a reply draft and runs the policy gate.

```bash
PYTHONPATH=src python3 -m alex_clone.cli draft-reply \
  --group "AI實戰先鋒會 AI Agent group" \
  --message "收到，我晚點整理給大家"
```

### `personal-line-send-plan`

Creates the Computer Use execution steps for Alex's personal LINE. If the group
is not approved or the policy requires confirmation, it stops before a send.

```bash
PYTHONPATH=src python3 -m alex_clone.cli personal-line-send-plan \
  --group "AI實戰先鋒會 AI Agent group" \
  --message "收到，我晚點整理給大家"
```

After Alex confirms an `ask_confirm` draft:

```bash
PYTHONPATH=src python3 -m alex_clone.cli personal-line-send-plan \
  --group "AI實戰先鋒會 AI Agent group" \
  --message "收到，我晚點整理給大家" \
  --confirmed \
  --audit
```

## Tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

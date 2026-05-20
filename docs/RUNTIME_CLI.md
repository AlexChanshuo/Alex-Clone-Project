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

### `interpret-command`

Parses Telegram-style natural language into an intent, tags, group matches, and
reply text.

```bash
PYTHONPATH=src python3 -m alex_clone.cli interpret-command "分身，去看 AI 群今天有什麼重要的"
PYTHONPATH=src python3 -m alex_clone.cli interpret-command "整理 BNI 今天重點並更新 alex-mind"
```

### `command-plan`

Turns a Telegram-style natural-language command into target groups, fetch
plans, and the next runtime step.

```bash
PYTHONPATH=src python3 -m alex_clone.cli command-plan "分身，去看 AI 群今天有什麼重要的"
PYTHONPATH=src python3 -m alex_clone.cli command-plan "整理 BNI 今天重點並更新 alex-mind"
```

### `guide`

Shows command examples for Alex.

```bash
PYTHONPATH=src python3 -m alex_clone.cli guide
```

### `fetch-plan`

Creates the exact plan the future Computer Use LINE fetcher must follow. This
does not click LINE yet; it tells the executor which group to open, how many
scrolls are allowed, where the checkpoint is, and what safety checks are
required.

```bash
PYTHONPATH=src python3 -m alex_clone.cli fetch-plan --tag AI
PYTHONPATH=src python3 -m alex_clone.cli fetch-plan --tag BNI --max-scrolls 4 --capture-limit 40
PYTHONPATH=src python3 -m alex_clone.cli fetch-plan --group "AI實戰先鋒會 AI Agent group"
```

### `checkpoints`

Shows the last successfully ingested point for each approved LINE group.

```bash
PYTHONPATH=src python3 -m alex_clone.cli checkpoints
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
PYTHONPATH=src python3 -m alex_clone.cli ingest-manual tests/fixtures/line_events.jsonl --new-only --update-checkpoint
```

### `normalize-capture`

Converts a LINE screen capture JSON file into normalized `LineEvent` JSONL.
This is the contract for the future Computer Use reader.

```bash
PYTHONPATH=src python3 -m alex_clone.cli normalize-capture \
  tests/fixtures/line_capture_ai.json \
  --group "AI實戰先鋒會"
```

Capture JSON shape:

```json
{
  "source": "line_personal_computer_use",
  "group_title": "AI實戰先鋒會",
  "captured_at": "2026-05-20T22:10:00+08:00",
  "messages": [
    {
      "sender": "Kevin",
      "sent_at": "2026-05-20T22:01:00+08:00",
      "text": "請問 Alex 可以幫我看一下 AI agent demo 嗎？"
    }
  ]
}
```

### `ingest-capture`

Normalizes a capture, writes raw events to `alex-mind`, updates the checkpoint,
and can produce a report.

```bash
PYTHONPATH=src python3 -m alex_clone.cli ingest-capture \
  tests/fixtures/line_capture_ai.json \
  --group "AI實戰先鋒會" \
  --new-only \
  --update-checkpoint \
  --report
```

For tests, redirect both vault and state:

```bash
ALEX_MIND_VAULT_DIR=/tmp/alex-clone-vault-test \
ALEX_CLONE_STATE_DIR=/tmp/alex-clone-state-test \
PYTHONPATH=src python3 -m alex_clone.cli ingest-capture \
  tests/fixtures/line_capture_ai.json \
  --group "AI實戰先鋒會" \
  --new-only \
  --update-checkpoint
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

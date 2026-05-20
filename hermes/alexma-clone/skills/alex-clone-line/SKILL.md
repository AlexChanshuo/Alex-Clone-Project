---
name: alex-clone-line
description: >
  Operate Alex Clone's LINE group intelligence backend: parse Telegram commands,
  plan personal LINE fetches, normalize capture JSON, ingest captures into
  alex-mind, check checkpoints, list groups, and guide Alex in Traditional Chinese.
version: 1.3.0
metadata:
  hermes:
    tags: [alex-clone, line, telegram, obsidian, alex-mind]
    category: personal-automation
---

# Alex Clone LINE

Use this skill whenever Alex asks to inspect, summarize, follow up on, or draft
replies for approved LINE groups.

Examples:

- `掃 AI 群`
- `看 BNI 今天有什麼重要的`
- `整理 AI 並更新 alex-mind`
- `檢查 family 有沒有需要我回`
- `幫我草擬回 AI 群：我晚點整理資料`
- `群組列表`
- `教我怎麼用`

## Principle

Hermes is the conversational brain. The Alex Clone Python CLI is the
deterministic execution layer.

Do not directly write vault files from the LLM. Prefer CLI commands that
validate, write, checkpoint, and report.

Do not edit this skill or its reference files during normal Telegram operation.
Runtime notes belong in ignored session files or the `alex-mind` vault.

## Repo Root

```text
/Users/alex/Documents/New project/Alex-Clone-Project
```

## Canonical Procedure

1. Parse Alex's message naturally. He should not need exact commands.
2. Run `command-plan` to get target groups, tags, fetch plans, and next step:

```bash
PYTHONPATH=src python3 -m alex_clone.cli command-plan "<Alex message>"
```

3. Explain the interpreted action in concise Traditional Chinese.
4. If the plan requires live LINE reading, tell Alex which group/tag will be
   checked and that the Computer Use reader must execute the fetch plan.
5. If a capture JSON file is available, ingest it:

```bash
PYTHONPATH=src python3 -m alex_clone.cli ingest-capture <capture.json> --group "<group or alias>" --new-only --update-checkpoint --report
```

6. If Alex asks for help, run:

```bash
PYTHONPATH=src python3 -m alex_clone.cli guide
```

7. If Alex asks which groups are watched:

```bash
PYTHONPATH=src python3 -m alex_clone.cli groups
```

## Useful Commands

```bash
PYTHONPATH=src python3 -m alex_clone.cli groups --tag AI
PYTHONPATH=src python3 -m alex_clone.cli groups --tag BNI
PYTHONPATH=src python3 -m alex_clone.cli fetch-plan --tag AI
PYTHONPATH=src python3 -m alex_clone.cli checkpoints
PYTHONPATH=src python3 -m alex_clone.cli normalize-capture tests/fixtures/line_capture_ai.json --group "AI實戰先鋒會"
```

## Live-Capture Safety Checklist

- Before opening or operating Alex's LINE UI, show the target group title and
  ask Alex for confirmation if there is any ambiguity.
- Verify the active LINE group title before reading or sending.
- Use screenshots or OCR only as aids; do not rely on them alone for safety
  checks.
- Do not send LINE messages from Hermes directly until the Computer Use executor
  is implemented and title-checked.
- Stop and report if a permission, payment, login, 2FA, or system dialog appears.
- Respect `capture_limit` and `max_scrolls`; do not endlessly scroll.
- If `validate_group_title()` raises a title mismatch, halt the
  ingest pipeline and require a fresh capture or explicit human confirmation
  that the captured screenshot belongs to the intended group.

## Ingest Success Proof

Do not claim LINE ingest is complete unless the CLI result shows all of the
following as explicit evidence:

- `events_ingested` is > 0 when new events were expected, or the CLI JSON
  explicitly explains why zero events were ingested (e.g. checkpoint covered them).
- `paths` includes one or more written vault/raw event files.
- `updated_checkpoints` includes the affected group when checkpointing was requested.
- the group title matched the approved group or alias.

If `--new-only` returns zero new events, do this before retrying:
1. Run `PYTHONPATH=src python3 -m alex_clone.cli checkpoints`.
2. If those messages are not newer, skip or ask before re-ingesting older messages.
3. Re-run without `--new-only` only after human approval.

If the CLI returns `report_markdown` but no `paths` or checkpoint updates, treat
it as a partial operation and ask before claiming completion.

## Telegram Report Output

- Send Alex a concise Traditional Chinese summary in the Telegram message body.
- Do not attach local Markdown, JSON, JSONL, screenshots, or placeholder paths
  unless Alex explicitly asks for the file.
- If a report was saved, mention only the saved vault path and the proof fields:
  `events_ingested`, `paths`, `updated_checkpoints`, `report_path`.
- Never describe a report as complete when it only contains placeholders such as
  "None detected" for messages that contain requests like `請`, `測試`, `回覆`,
  `幫`, or `確認`.

## Reply/Sending Safety

If Alex asks you to reply:

1. Draft the reply first.
2. Mention target group.
3. Ask for confirmation unless policy explicitly allows auto-send.
4. Use `personal-line-send-plan` only after Alex confirms.

## Response Style

Reply in concise Traditional Chinese with practical status:

```text
我理解你要掃 AI 群。
目標群組：AI實戰先鋒會 AI Agent group
下一步：打開 Alex 本人的 LINE，確認群組標題，讀取 checkpoint 之後的新訊息。
目前我會先產生 fetch plan；真正讀 LINE UI 的 Computer Use reader 是下一步。
```

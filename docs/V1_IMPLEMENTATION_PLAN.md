# V1 Implementation Plan

This is the build plan after the three planning cycles. It is intentionally
read-first and confirmation-first so the clone becomes useful before it becomes
powerful.

## Target User Command

```text
分身，整理今天群裡的重要進度，更新 alex-mind，提醒我需要回誰。
```

Expected result:

- group-by-group summary,
- open loops and people to reply to,
- calendar conflicts if any,
- vault updates written,
- suggested replies drafted,
- no LINE reply sent unless Alex confirms or policy allows it.

## Phase 0: Project Setup

Status: scaffolded.

Tasks:

- Keep this repo separate from BNI Masta.
- Use `/Users/alex/Documents/Alex-Clone/Alex-Mind` as the canonical vault.
- Keep `.env` local and untracked.
- Create group and policy config files from examples.
- Add source links and research decisions to docs.

## Phase 1: LINE Read Pipeline

Status: scaffolded for manual JSONL captures, LINE screen capture JSON,
personal LINE fetch plans, command plans, checkpoints, and personal LINE send
plans.

Build one ingestion abstraction with three adapters. V1 uses Alex's personal
LINE session on this Mac as the primary route.

| Adapter | Priority | Notes |
|---|---:|---|
| `line_personal_computer_use` | 1 | Uses Alex's logged-in LINE desktop/web UI on this Mac |
| `line_webhook` | 2 | Optional later path when a clone OA is invited to a group |
| `manual_import` | 3 | Paste/export/import historical messages |

Capture JSON is now the contract between Computer Use and the ingest pipeline.
The UI reader should output:

```json
{
  "source": "line_personal_computer_use",
  "group_title": "AI實戰先鋒會",
  "captured_at": "2026-05-20T22:10:00+08:00",
  "messages": [
    {
      "sender": "Kevin",
      "sent_at": "2026-05-20T22:01:00+08:00",
      "text": "message body"
    }
  ]
}
```

Normalized event shape:

```json
{
  "source": "line_personal_computer_use",
  "group_id": "local-line-group-alias-or-detected-name",
  "group_name": "AI實戰先鋒會 AI Agent group",
  "message_id": "provider-message-id",
  "sender_id": "line-user-or-observed-name",
  "sender_name": "display name if available",
  "sent_at": "2026-05-20T20:30:00+08:00",
  "type": "text",
  "text": "message body",
  "confidence": 1.0
}
```

## Phase 2: alex-mind Vault Writer

Status: scaffolded.

The writer should follow the existing `alex-mind` rules from `CLAUDE.md`:

- raw source first,
- classify,
- ingest into wiki,
- append dated entries,
- use `[unverified]` when unsure,
- triage low-confidence facts.

Planned paths:

```text
raw/inbox/line/YYYY-MM-DD/<group-slug>.jsonl
wiki/syntheses/interactions-rolling/YYYY-MM-DD-line-digest.md
wiki/outputs/alex-clone-daily/YYYY-MM-DD.md
wiki/outputs/triage-queue.md
```

Do not create a second vault. Do not write clone memory into BNI Masta unless
Alex explicitly asks for a one-off export.

Checkpoint state is stored outside Git at:

```text
.alex-clone-state/line-checkpoints.json
```

This is operational state, not memory. It should not be committed.

## Phase 3: Daily Report Engine

Status: scaffolded.

Cadence:

| Time | Routine | Purpose |
|---|---|---|
| 09:00 | Morning brief | Overnight changes, urgent replies, calendar risks |
| 12:30 | Midday pulse | Open loops and time-sensitive asks |
| 20:00 | Night report | Two-level summary: per-group plus personal diary |

Report sections:

- `今天群裡發生什麼`
- `誰需要 Alex 回`
- `有哪些承諾/待辦`
- `跟行事曆有沒有衝突`
- `已更新 alex-mind 哪些筆記`
- `建議回覆草稿`

## Phase 4: Google Calendar Context

Start with read-only:

- list upcoming events,
- query free/busy windows,
- detect conflicts before reply drafting,
- include calendar assumptions in the draft summary.

Write later with confirmation:

```text
Alex: 幫我排週五 15:00 跟 Kevin 開會。
Clone: 我看到週五 15:00-16:00 可行。是否建立 Google Calendar 事件？
Alex: confirm
Clone: creates event and logs outcome.
```

## Phase 5: Reply Drafting And Sending

Status: drafting and send-plan scaffolded; live UI execution is next.

Every candidate reply should carry:

- target group,
- target person if known,
- source message or reason,
- draft text,
- risk level,
- whether calendar was checked,
- send policy decision.

Default actions:

| Command Style | Behavior |
|---|---|
| "幫我回..." | Draft and ask confirmation |
| "確認送出" | Send the approved draft |
| "以後這種可以直接回" | Add only if group policy allows low-risk auto-send |
| "幫我安排/答應..." | Check calendar and ask confirmation |

Because V1 uses Alex's personal LINE identity, the executor must verify the
active group title before any send, paste the prepared message, take a
pre-send or post-send screenshot when practical, and write an audit record.

## Phase 6: Automation

Create recurring jobs only after Phase 1-5 work manually:

- `09:00` morning brief,
- `12:30` pulse,
- `20:00` night report,
- optional weekly relationship rollup.

Each job should report to Alex, not silently modify external conversations.

## Acceptance Tests

Before calling V1 live:

- Add one approved LINE test group.
- Capture ten messages into raw inbox.
- Generate one daily report.
- Write one digest to `alex-mind`.
- Draft one reply without sending.
- Confirm-send one reply and log the audit.
- Query calendar free/busy for one proposed meeting.
- Verify no secrets were committed.

## Open Questions

- Which LINE groups can invite the clone Official Account?
- Which personal LINE groups should be approved for V1 monitoring?
- Should morning and night reports go to LINE, Telegram, or a private note first?
- What reply categories should be auto-send eligible after V1?
- Should the clone identify itself in each group, or only in test messages?

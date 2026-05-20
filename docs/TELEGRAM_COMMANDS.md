# Telegram Commands

Alex Clone is controlled from Telegram through `@AlexmaClone_bot`. Telegram is
the command surface; Alex's personal LINE on this Mac is the workspace the clone
operates.

The recommended live Telegram runtime is Hermes Agent. Hermes provides the
LLM-backed conversation layer; Alex Clone's Python CLI remains the deterministic
execution layer.

Current status: Hermes is installed and paired for Alex's Telegram account. The
gateway has been tested manually; persistent service setup is the next runtime
step.

Bot URL:

<https://t.me/AlexmaClone_bot>

## Local Secret

The bot token belongs only in local `.env`:

```text
ALEX_CLONE_TELEGRAM_BOT_TOKEN=
TELEGRAM_BOT_TOKEN=
```

Do not commit `.env`.

## Execution Keywords

The parser intentionally accepts wide Chinese and English wording.

### Scan / Fetch

- `掃 AI 群`
- `去看 BNI 群`
- `檢查 family`
- `watch Friends`
- `scan AI`
- `monitor BNI`
- `抓今天 AI 群訊息`

### Summarize / Report

- `整理 AI 群今天重點`
- `總結 BNI`
- `做 Friends 懶人包`
- `AI digest`
- `BNI summary`
- `今天誰需要我回`

### Vault / Memory

- `更新 alex-mind`
- `寫進 vault`
- `存到 vault`
- `把今天 AI 群重點存起來`
- `save memory`
- `update vault`

### Reply Drafting

- `幫我草擬回 AI 群：我晚點整理資料`
- `幫我回 BNI：收到，我會確認`
- `write reply to Friends: I will check later`
- `reply draft`

### Send Confirmation

- `確認送出`
- `可以發`
- `發出去`
- `send it`
- `confirm`

### Guidance

- `指令`
- `怎麼用`
- `教我`
- `help`
- `guide`
- `群組列表`

## Tags

| Tag | Meaning |
|---|---|
| `BNI` | BNI chapter, referrals, PALMS, meetings, member follow-up |
| `AI` | AI news, agent projects, tools, community discussion |
| `family` | Family logistics and personal care context |
| `Friends` | Friends and social follow-up |

## CLI Test

```bash
PYTHONPATH=src python3 -m alex_clone.cli interpret-command "分身，去看 AI 群今天有什麼重要的"
PYTHONPATH=src python3 -m alex_clone.cli guide
```

## Hermes Live Test

After the gateway is running, message the bot naturally:

```text
分身，去看 AI 群今天有什麼重要的
```

Expected current behavior:

- Hermes understands the intent.
- It identifies the approved `AI` group target.
- It explains that the LINE Computer Use reader is the next executor.
- It should not claim that it already read LINE until the capture reader exists.

## Report Quality Rule

When Alex asks for a report, the bot should answer in Telegram with a concise
Traditional Chinese summary. It should not attach raw Markdown/JSON files unless
Alex explicitly asks for files. A valid report should mention proof fields from
the CLI result, especially `events_ingested`, `paths`, `updated_checkpoints`,
and `report_path` when saved.

The report generator should treat words like `請`, `測試`, `回覆`, `幫`, and
`確認` as possible action items. It should not say "no tasks" when those words
appear in captured LINE messages.

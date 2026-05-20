# Hermes Integration

Alex Clone uses Hermes Agent as the recommended LLM-backed Telegram brain.

## Why Hermes

Research sources:

- Hermes docs describe it as an agent with native Telegram and 15+ messaging
  gateway support, skills, persistent memory, tools, MCP, and cron automation:
  <https://hermes-agent.nousresearch.com/docs/>
- Hermes `SOUL.md` is the primary durable identity file loaded from
  `HERMES_HOME`: <https://hermes-agent.nousresearch.com/docs/user-guide/features/personality>
- Hermes Telegram setup uses BotFather tokens and `TELEGRAM_ALLOWED_USERS`:
  <https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram>
- Hermes skills are Markdown files with YAML frontmatter under
  `~/.hermes/skills/` or the active Hermes home:
  <https://hermes-agent.nousresearch.com/docs/guides/work-with-skills/>

This matches Alex's existing AlexMind architecture: deterministic capture and
vault writes, LLM for understanding and conversation.

## Architecture

```text
Telegram @AlexmaClone_bot
        ↓
Hermes Agent brain
        ↓
alex-clone-line skill
        ↓
Alex Clone Python CLI
        ↓
Personal LINE / alex-mind vault
```

Hermes should talk naturally with Alex. The Python CLI should handle execution:

- command parsing fallback,
- group watchlist,
- fetch plans,
- capture normalization,
- checkpoint updates,
- vault writes,
- report generation,
- send policy.

## Files Added

```text
hermes/alexma-clone/
  SOUL.md
  USER.md
  MEMORY.md
  AGENTS.md
  config.example.yaml
  skills/alex-clone-line/SKILL.md
  skills/alex-clone-line/references/cli.md
  hooks/auto-save-inbox/README.md
scripts/setup_hermes_alexma_clone.sh
```

## Current Live Status

As of 2026-05-21:

- Hermes is installed locally at `~/.local/bin/hermes`.
- `HERMES_HOME` is `/Users/alex/Documents/New project/Alex-Clone-Project/hermes/alexma-clone`.
- `config.yaml` is present locally and uses Copilot `gpt-5-mini` as the model.
- Telegram pairing has been approved for Alex's Telegram account.
- The gateway has been tested and `hermes status` reports it running through
  `launchd`.
- The LINE Computer Use reader is still the next build phase; Hermes can plan
  and guide the operation, but it does not yet complete daily LINE reports
  end-to-end by itself.

## Setup

Hermes is not committed into this repo. Install it from the official installer:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

Then run:

```bash
cd "/Users/alex/Documents/New project/Alex-Clone-Project"
bash scripts/setup_hermes_alexma_clone.sh
export HERMES_HOME="/Users/alex/Documents/New project/Alex-Clone-Project/hermes/alexma-clone"
```

Make sure the local, ignored file exists:

```text
hermes/alexma-clone/.env
```

It should contain:

```text
TELEGRAM_BOT_TOKEN=...
TELEGRAM_ALLOWED_USERS=<Alex numeric Telegram user id>
ALEX_MIND_VAULT_DIR=/Users/alex/Documents/Alex-Clone/Alex-Mind
ALEX_CLONE_GROUPS_CONFIG=/Users/alex/Documents/New project/Alex-Clone-Project/config/groups.json
ALEX_CLONE_STATE_DIR=/Users/alex/Documents/New project/Alex-Clone-Project/.alex-clone-state
```

Do not commit `.env`.

## Running

After Hermes is installed and configured:

```bash
export HERMES_HOME="/Users/alex/Documents/New project/Alex-Clone-Project/hermes/alexma-clone"
hermes gateway setup
hermes gateway
```

For a persistent Mac service:

```bash
hermes gateway install
hermes gateway start
hermes gateway status
```

If the service needs to be reinstalled or restarted:

```bash
export PATH="$HOME/.local/bin:$PATH"
export HERMES_HOME="/Users/alex/Documents/New project/Alex-Clone-Project/hermes/alexma-clone"
hermes gateway install
hermes gateway start
hermes gateway status
```

## Test the Backend Skill Contract

Before live Telegram:

```bash
PYTHONPATH=src python3 -m alex_clone.cli command-plan "分身，去看 AI 群今天有什麼重要的"
PYTHONPATH=src python3 -m alex_clone.cli groups
PYTHONPATH=src python3 -m alex_clone.cli checkpoints
```

Expected behavior:

- Hermes understands natural language.
- The `alex-clone-line` skill calls the CLI.
- The CLI returns target groups and fetch plans.
- Hermes explains the next step in friendly Chinese.

## Still Not Done

Hermes integration gives the LLM-backed Telegram brain. It does not yet solve:

- live Computer Use LINE reading,
- clicking/sending inside LINE,
- Google Calendar integration.

Those remain separate backend phases.

## Next Phase

Build the Computer Use LINE fetcher:

1. Open Alex's personal LINE on this Mac.
2. Select only an approved group from `config/groups.json`.
3. Verify the visible group title before reading.
4. Capture visible messages and scroll up until the checkpoint.
5. Emit capture JSON for the existing `ingest-capture` CLI.
6. Write raw events and daily reports to `alex-mind`.
7. Return a concise Telegram summary through Hermes.

Before scheduling daily reports, verify the gateway remains healthy after Mac
sleep/restart:

```bash
export PATH="$HOME/.local/bin:$PATH"
export HERMES_HOME="/Users/alex/Documents/New project/Alex-Clone-Project/hermes/alexma-clone"
hermes gateway status
```

# Alex Clone Project

Alex Clone Project is the operating system for Alex's authorized digital double.
The clone is meant to sit in selected LINE groups, collect useful context, report
back to Alex, maintain the `alex-mind` Obsidian vault, understand calendar
constraints, and help draft or send replies only under Alex's rules.

This project is separate from BNI Masta. It may reuse patterns from BNI Masta
later, but it owns its own repo, docs, config, vault namespace, and release path.

## Mission

Build a trusted Alex 分身 that can:

- join LINE groups where the real Alex intentionally adds it,
- observe group progress and summarize what matters,
- produce daily reports per group,
- update the `alex-mind` Obsidian vault with relationship and project memory,
- read Alex's schedule from Google Calendar when authorized,
- prepare reply drafts in Alex's voice,
- send LINE replies only when explicitly commanded or allowlisted,
- keep a personal diary note for Alex,
- preserve privacy, consent, and auditability.

## Core Principle

The clone is not a hidden impersonation bot. It is an authorized assistant that
acts for Alex in approved spaces, with clear target allowlists and logs.

## Planned Daily Rhythm

| Time | Routine | Output |
|---|---|---|
| 09:00 | Morning scan | overnight group changes, calendar conflicts, priority replies |
| 12:30 | Midday pulse | urgent group requests, unanswered mentions, schedule nudges |
| 20:00 | Daily report | per-group summary, relationship updates, diary note |
| On command | Reply/send | draft first by default, auto-send only for allowlisted low-risk patterns |

## Initial Capabilities

| Capability | Status | Notes |
|---|---|---|
| LINE group monitoring | scaffold | personal LINE Computer Use is the V1 route |
| Daily group report | scaffold | JSONL event captures can generate Markdown reports |
| `alex-mind` vault updates | scaffold | raw captures, reports, digests, and send audits |
| Google Calendar awareness | design | needs connector/auth before live use |
| Reply drafting | scaffold | policy-gated CLI draft command exists |
| Reply sending | scaffold | personal LINE send-plan command exists, UI execution next |
| Personal diary | design | daily private note for Alex |

## Follow-Up Group Tags

The clone supports follow-up tags for watched LINE groups:

- `BNI`
- `AI`
- `family`
- `Friends`

The real approved watchlist lives locally in `config/groups.json` and is ignored
by Git. Current local V1 watchlist has one BNI group and one AI group.

## Repo Structure

```text
docs/              Architecture, product scope, operating policies
src/               Future runtime code
config/            Non-secret config templates
vault-templates/   Markdown templates for the alex-mind Obsidian vault
```

## Canonical Memory Vault

The LLM wiki vault for this project is:

```text
/Users/alex/Documents/Alex-Clone/Alex-Mind
```

In docs and config this is referred to as `alex-mind`. The clone should write
raw LINE captures, daily summaries, relationship notes, diary entries, and task
memory there, following the vault's existing append-first rules.

## Planning Docs

- [Three-cycle plan](docs/PLANNING_CYCLES.md)
- [V1 implementation plan](docs/V1_IMPLEMENTATION_PLAN.md)
- [Runtime CLI](docs/RUNTIME_CLI.md)
- [Telegram commands](docs/TELEGRAM_COMMANDS.md)
- [Architecture](docs/ARCHITECTURE.md)
- [LINE workflows](docs/LINE_WORKFLOWS.md)
- [Calendar workflows](docs/CALENDAR_WORKFLOWS.md)
- [Vault schema](docs/VAULT_SCHEMA.md)
- [Operating policy](docs/OPERATING_POLICY.md)

## Safety Rules

- No secrets in GitHub.
- No hidden monitoring outside groups Alex explicitly adds/approves.
- No auto-reply in new groups until Alex approves the group policy.
- No sensitive personal data sent outside its source group without permission.
- All sends and vault writes should be audit logged.

## Next Build Milestones

1. Create real local `config/groups.json` with approved personal LINE groups.
2. Connect Computer Use to execute `PersonalLineSendPlan` safely.
3. Add calendar reader with Google Calendar connector.
4. Improve Alex voice drafting with examples from `alex-mind`.
5. Add daily scheduled reports.
6. Add eval fixtures from real approved group captures.

## Run V1 Locally

```bash
PYTHONPATH=src python3 -m alex_clone.cli status
PYTHONPATH=src python3 -m alex_clone.cli daily-report tests/fixtures/line_events.jsonl --date 2026-05-20
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

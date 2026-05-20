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
| LINE group monitoring | design | groups must be added/approved by Alex |
| Daily group report | design | one report per group plus master summary |
| `alex-mind` vault updates | design | append-only notes first, structured memory later |
| Google Calendar awareness | design | needs connector/auth before live use |
| Reply drafting | design | Alex voice guide required |
| Reply sending | design | confirmation-gated except allowlisted commands |
| Personal diary | design | daily private note for Alex |

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

1. Define group allowlist and LINE access model.
2. Create Alex voice and reply policy.
3. Add vault writer for daily notes.
4. Add calendar reader with Google Calendar connector.
5. Add LINE executor path for approved groups.
6. Add daily scheduled reports.

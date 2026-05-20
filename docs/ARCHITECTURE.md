# Architecture

## High-Level Flow

```mermaid
flowchart TD
  A["Approved LINE groups"] --> B["Ingestion"]
  B --> C["Event classifier"]
  C --> D["Group memory"]
  C --> E["Tasks and open loops"]
  C --> F["Reply candidates"]
  G["Google Calendar"] --> H["Schedule context"]
  D --> I["Daily report generator"]
  E --> I
  H --> I
  F --> J["Reply policy gate"]
  J --> K["Draft to Alex"]
  J --> L["Send via LINE executor"]
  I --> M["alex-mind Obsidian vault"]
```

## Components

| Component | Responsibility |
|---|---|
| Ingestion | Capture messages/events from approved LINE groups |
| Event classifier | Convert raw chat into mentions, tasks, decisions, social signals |
| Memory writer | Append structured notes to the `alex-mind` Obsidian vault |
| Calendar context | Read free/busy and upcoming events |
| Reply drafter | Produce Alex-style replies with rationale |
| Policy gate | Decide draft-only, ask-confirmation, or auto-send |
| LINE executor | Send via approved LINE route and write delivery audit |
| Scheduler | Run morning/midday/night routines |

## Ingestion Adapters

| Adapter | When To Use |
|---|---|
| LINE Official Account webhook | Preferred path when the clone OA can be added to the group |
| Computer Use over LINE desktop/web | Fallback for groups that must use Alex's logged-in LINE UI |
| Manual import | Historical catch-up or one-off exports |

## Storage Model

Vault-first, append-only in V1. The canonical LLM wiki vault is named
`alex-mind`; do not write clone memory into the BNI vault.

```text
alex-mind/
  daily/
    YYYY-MM-DD.md
  line-groups/
    <group-slug>.md
  people/
    <person-name>.md
  tasks/
    open-loops.md
  logs/
    line-send-audit/YYYY-MM-DD.jsonl
```

Structured database can be added later after the note schema stabilizes.

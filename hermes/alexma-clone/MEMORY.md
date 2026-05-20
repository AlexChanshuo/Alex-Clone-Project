# Memory

Durable facts for Alexma Clone:

- Use `alex-mind` as the canonical personal memory vault.
- Real LINE group watchlist is local-only at `config/groups.json`.
- Supported follow-up tags: `BNI`, `AI`, `family`, `Friends`.
- Current local approved groups:
  - `BNI華AI名人堂分會` tagged `BNI`
  - `AI實戰先鋒會 AI Agent group` tagged `AI`
- The Alex Clone backend is deterministic Python under `src/alex_clone`.
- Before live LINE UI automation exists, use `command-plan`, `fetch-plan`,
  `normalize-capture`, and `ingest-capture` as the safe bridge.
- The next implementation blocker is the Computer Use LINE reader that produces
  capture JSON from the visible LINE UI.


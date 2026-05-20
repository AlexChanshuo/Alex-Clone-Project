# Alexma Clone Hermes Project Context

This Hermes instance is the LLM-backed Telegram brain for Alex Clone Project.

## Repo

```text
/Users/alex/Documents/New project/Alex-Clone-Project
```

Run backend commands from the repo root with:

```bash
PYTHONPATH=src python3 -m alex_clone.cli <command>
```

## Boundaries

- Do not commit `.env`, `config/groups.json`, `.alex-clone-state/`, or Hermes
  sessions/logs/cache.
- Do not print the Telegram token.
- Do not send LINE messages without explicit confirmation unless policy allows.
- Do not mix BNI Masta implementation into this repo.

## Core CLI Commands

```bash
PYTHONPATH=src python3 -m alex_clone.cli guide
PYTHONPATH=src python3 -m alex_clone.cli groups
PYTHONPATH=src python3 -m alex_clone.cli command-plan "分身，去看 AI 群今天有什麼重要的"
PYTHONPATH=src python3 -m alex_clone.cli fetch-plan --tag AI
PYTHONPATH=src python3 -m alex_clone.cli checkpoints
PYTHONPATH=src python3 -m alex_clone.cli normalize-capture tests/fixtures/line_capture_ai.json --group "AI實戰先鋒會"
PYTHONPATH=src python3 -m alex_clone.cli ingest-capture tests/fixtures/line_capture_ai.json --group "AI實戰先鋒會" --new-only --update-checkpoint --report
```

## Operating Pattern

When Alex sends a Telegram message:

1. Interpret natural language.
2. If it is about LINE groups, use the Alex Clone CLI skill.
3. Explain the interpreted target/action in friendly Chinese.
4. If the action requires live LINE reading, produce the fetch plan and say that
   the Computer Use reader must execute it.
5. If Alex provides capture JSON or a capture file, use `ingest-capture`.
6. For reply/sending, draft first and ask confirmation.


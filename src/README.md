# Source

Runtime code for Alex Clone V1 lives in the `alex_clone` package.

## Modules

- `config.py` loads group policy, runtime policy, and the `alex-mind` vault path.
- `models.py` defines normalized LINE events, reply drafts, and send audits.
- `io.py` reads/writes JSONL event captures.
- `vault.py` writes raw captures, daily reports, rolling digests, and send audits.
- `report.py` generates first-pass daily group reports.
- `policy.py` decides draft-only, ask-confirm, auto-send, or blocked.
- `line_personal.py` creates personal LINE Computer Use execution plans.
- `cli.py` exposes the V1 command line.

## Local Commands

Run from the repo root:

```bash
PYTHONPATH=src python3 -m alex_clone.cli status
PYTHONPATH=src python3 -m alex_clone.cli daily-report tests/fixtures/line_events.jsonl --date 2026-05-20
PYTHONPATH=src python3 -m alex_clone.cli draft-reply --group "AI實戰先鋒會 AI Agent group" --message "收到，我晚點整理給大家"
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The personal LINE send path intentionally produces a plan first. It should not
drive the UI until the group is approved and the policy gate allows it.

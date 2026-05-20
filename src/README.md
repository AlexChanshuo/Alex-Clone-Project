# Source

Runtime code for Alex Clone V1 lives in the `alex_clone` package.

## Modules

- `config.py` loads group policy, runtime policy, and the `alex-mind` vault path.
- `models.py` defines normalized LINE events, reply drafts, and send audits.
- `checkpoint.py` stores local LINE fetch checkpoints.
- `line_capture.py` normalizes LINE screen capture JSON into `LineEvent`.
- `io.py` reads/writes JSONL event captures.
- `vault.py` writes raw captures, daily reports, rolling digests, and send audits.
- `report.py` generates first-pass daily group reports.
- `policy.py` decides draft-only, ask-confirm, auto-send, or blocked.
- `line_personal.py` creates personal LINE Computer Use fetch/send plans.
- `cli.py` exposes the V1 command line.

## Local Commands

Run from the repo root:

```bash
PYTHONPATH=src python3 -m alex_clone.cli status
PYTHONPATH=src python3 -m alex_clone.cli fetch-plan --tag AI
PYTHONPATH=src python3 -m alex_clone.cli command-plan "分身，去看 AI 群今天有什麼重要的"
PYTHONPATH=src python3 -m alex_clone.cli normalize-capture tests/fixtures/line_capture_ai.json --group "AI實戰先鋒會"
PYTHONPATH=src python3 -m alex_clone.cli checkpoints
PYTHONPATH=src python3 -m alex_clone.cli daily-report tests/fixtures/line_events.jsonl --date 2026-05-20
PYTHONPATH=src python3 -m alex_clone.cli draft-reply --group "AI實戰先鋒會 AI Agent group" --message "收到，我晚點整理給大家"
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The personal LINE send path intentionally produces a plan first. It should not
drive the UI until the group is approved and the policy gate allows it.

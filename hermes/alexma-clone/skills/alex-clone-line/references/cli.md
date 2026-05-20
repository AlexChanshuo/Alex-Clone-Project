# Alex Clone CLI Reference

Run from repo root:

```bash
cd "/Users/alex/Documents/New project/Alex-Clone-Project"
```

## Guide

```bash
PYTHONPATH=src python3 -m alex_clone.cli guide
```

## Interpret/Plan

```bash
PYTHONPATH=src python3 -m alex_clone.cli interpret-command "分身，去看 AI 群今天有什麼重要的"
PYTHONPATH=src python3 -m alex_clone.cli command-plan "整理 BNI 今天重點並更新 alex-mind"
```

## Groups

```bash
PYTHONPATH=src python3 -m alex_clone.cli groups
PYTHONPATH=src python3 -m alex_clone.cli groups --tag AI
PYTHONPATH=src python3 -m alex_clone.cli groups --tag BNI
```

## Fetch Plans / Checkpoints

```bash
PYTHONPATH=src python3 -m alex_clone.cli fetch-plan --tag AI
PYTHONPATH=src python3 -m alex_clone.cli checkpoints
```

## Capture / Ingest

```bash
PYTHONPATH=src python3 -m alex_clone.cli normalize-capture tests/fixtures/line_capture_ai.json --group "AI實戰先鋒會"
PYTHONPATH=src python3 -m alex_clone.cli ingest-capture tests/fixtures/line_capture_ai.json --group "AI實戰先鋒會" --new-only --update-checkpoint --report
```


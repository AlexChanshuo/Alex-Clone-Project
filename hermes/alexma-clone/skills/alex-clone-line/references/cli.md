# Alex Clone CLI Reference

Run from repo root:

```bash
cd "/Users/alex/Documents/New project/Alex-Clone-Project"
```

## Guide

```bash
PYTHONPATH=src python3 -m alex_clone.cli guide
```

## Interpret / Plan

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

## Reply Draft / Send Plan

```bash
PYTHONPATH=src python3 -m alex_clone.cli draft-reply --group "AI實戰先鋒會" --text "我晚點整理資料"
PYTHONPATH=src python3 -m alex_clone.cli personal-line-send-plan --group "AI實戰先鋒會" --text "我晚點整理資料"
```

## Hermes Smoke Test

```bash
export PATH="$HOME/.local/bin:$PATH"
export HERMES_HOME="/Users/alex/Documents/New project/Alex-Clone-Project/hermes/alexma-clone"
hermes gateway status
hermes -z "用繁體中文回答，只回答：Alex Clone Hermes 可以思考了。"
```

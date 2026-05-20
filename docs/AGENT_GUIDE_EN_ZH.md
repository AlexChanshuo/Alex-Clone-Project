# Agent Guide / Agent 操作指南

This guide is for Codex or any future agent working on Alex Clone Project.

## English

### Project Identity

- Repo: `Alex-Clone-Project`
- Local path: `/Users/alex/Documents/New project/Alex-Clone-Project`
- GitHub: `https://github.com/AlexChanshuo/Alex-Clone-Project`
- Canonical memory vault: `/Users/alex/Documents/Alex-Clone/Alex-Mind`
- Telegram command bot: `@AlexmaClone_bot`
- LINE route: Alex's personal LINE on this Mac via Computer Use

This project is separate from BNI Masta. Do not mix BNI Masta implementation or
docs into this repo unless Alex explicitly asks.

### Current Runtime

The code is dependency-free Python under `src/alex_clone`.

Main modules:

- `commands.py`: parses Telegram-style natural language.
- `config.py`: loads `.env`, group config, policy config, and vault path.
- `line_personal.py`: creates safe LINE Computer Use send plans.
- `checkpoint.py`: stores LINE fetch checkpoints in local untracked state.
- `report.py`: creates daily reports from normalized LINE events.
- `vault.py`: writes raw captures, reports, digests, and audits to `alex-mind`.
- `policy.py`: decides draft-only, ask-confirm, auto-send, or blocked.
- `cli.py`: command-line harness.

### Local Secrets And Private Files

Never commit:

- `.env`
- `config/groups.json`
- any real LINE screenshots containing private content unless Alex explicitly
  asks and the repo target is private.

The bot token is local only. Do not print it in final responses.

### Real Group Watchlist

Use local `config/groups.json`. It is ignored by Git.

Current local groups:

- `BNI華AI名人堂分會`, tag `BNI`
- `AI實戰先鋒會 AI Agent group`, tag `AI`

Supported tags:

- `BNI`
- `AI`
- `family`
- `Friends`

### Commands To Verify

Run from repo root:

```bash
PYTHONPATH=src python3 -m alex_clone.cli status
PYTHONPATH=src python3 -m alex_clone.cli groups
PYTHONPATH=src python3 -m alex_clone.cli interpret-command "分身，去看 AI 群今天有什麼重要的"
PYTHONPATH=src python3 -m alex_clone.cli fetch-plan --tag AI
PYTHONPATH=src python3 -m alex_clone.cli checkpoints
PYTHONPATH=src python3 -m alex_clone.cli guide
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

### Intended Live Flow

1. Alex sends a Telegram command.
2. Command parser returns intent, tags, group matches, and reply text.
3. Runtime resolves tags to approved LINE groups.
4. Computer Use opens Alex's personal LINE.
5. Executor verifies the active group title before reading or sending.
6. Captured LINE messages become normalized `LineEvent` records.
7. `VaultWriter` saves raw events to `alex-mind/raw/inbox/line/`.
8. `CheckpointStore` updates `.alex-clone-state/line-checkpoints.json`.
9. Report generator creates daily summaries.
10. Reply drafts pass through the policy gate.
11. Sends require confirmation unless group policy explicitly allows auto-send.
12. Send audit is written to `alex-mind/logs/line-send-audit/`.

### Next Build Step

Build the Computer Use LINE fetcher:

- open LINE,
- select an approved group,
- verify title,
- read visible messages,
- scroll until checkpoint,
- normalize events,
- save checkpoint,
- write raw events to `alex-mind`,
- return summary to Telegram.

Do not build auto-send before read/fetch/checkpoint is stable.

Current next-phase status: fetch plans and checkpoints are implemented, but the
actual UI reader is still next.

## 中文

### 專案身份

- Repo：`Alex-Clone-Project`
- 本機路徑：`/Users/alex/Documents/New project/Alex-Clone-Project`
- GitHub：`https://github.com/AlexChanshuo/Alex-Clone-Project`
- 主要記憶 vault：`/Users/alex/Documents/Alex-Clone/Alex-Mind`
- Telegram 指令 bot：`@AlexmaClone_bot`
- LINE 操作方式：用 Computer Use 操作這台 Mac 上 Alex 本人的 LINE

這個專案跟 BNI Masta 是分開的。除非 Alex 明確要求，不要把 BNI Masta 的實作或文件混進這個 repo。

### 目前 runtime

程式碼是無外部依賴的 Python，位置在 `src/alex_clone`。

主要模組：

- `commands.py`：解析 Telegram 自然語言指令。
- `config.py`：讀 `.env`、群組 config、policy config、vault 路徑。
- `line_personal.py`：建立安全的 LINE Computer Use 操作計畫。
- `checkpoint.py`：把 LINE 擷取進度存在本機未追蹤 state。
- `report.py`：把標準化 LINE events 變成每日報告。
- `vault.py`：把 raw capture、report、digest、audit 寫進 `alex-mind`。
- `policy.py`：判斷 draft-only、ask-confirm、auto-send、blocked。
- `cli.py`：本機 CLI 測試入口。

### 本機秘密與私有檔案

絕對不要 commit：

- `.env`
- `config/groups.json`
- 任何含私人內容的 LINE 截圖，除非 Alex 明確要求且確認 repo 目標安全。

bot token 只能留在本機，不要在 final response 裡印出完整 token。

### 真實群組 watchlist

使用本機 `config/groups.json`。這個檔案已被 Git ignore。

目前本機群組：

- `BNI華AI名人堂分會`，標籤 `BNI`
- `AI實戰先鋒會 AI Agent group`，標籤 `AI`

支援標籤：

- `BNI`
- `AI`
- `family`
- `Friends`

### 驗證指令

在 repo root 執行：

```bash
PYTHONPATH=src python3 -m alex_clone.cli status
PYTHONPATH=src python3 -m alex_clone.cli groups
PYTHONPATH=src python3 -m alex_clone.cli interpret-command "分身，去看 AI 群今天有什麼重要的"
PYTHONPATH=src python3 -m alex_clone.cli fetch-plan --tag AI
PYTHONPATH=src python3 -m alex_clone.cli checkpoints
PYTHONPATH=src python3 -m alex_clone.cli guide
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

### 預期正式流程

1. Alex 在 Telegram 下指令。
2. command parser 回傳 intent、tags、group matches、reply text。
3. runtime 把 tags 對應到已核准 LINE 群。
4. Computer Use 打開 Alex 本人的 LINE。
5. executor 在讀取或送出前確認目前群組標題正確。
6. 擷取到的 LINE 訊息轉成標準 `LineEvent`。
7. `VaultWriter` 把 raw events 存到 `alex-mind/raw/inbox/line/`。
8. `CheckpointStore` 更新 `.alex-clone-state/line-checkpoints.json`。
9. report generator 產生每日摘要。
10. reply draft 通過 policy gate。
11. 除非群組 policy 明確允許 auto-send，否則送出前要 Alex 確認。
12. send audit 寫到 `alex-mind/logs/line-send-audit/`。

### 下一個開發步驟

建立 Computer Use LINE fetcher：

- 打開 LINE，
- 選擇已核准群組，
- 確認群組標題，
- 讀取可見訊息，
- 往上捲到 checkpoint，
- 標準化 events，
- 保存 checkpoint，
- 把 raw events 寫入 `alex-mind`，
- 回 Telegram 給 Alex 摘要。

在 read/fetch/checkpoint 穩定之前，不要先做 auto-send。

目前下一階段狀態：fetch plan 與 checkpoint 已完成，真正讀取 LINE UI 的 reader 還是下一步。

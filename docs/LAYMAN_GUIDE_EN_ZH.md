# Layman Guide / 白話指南

## English

Alex Clone is Alex's personal assistant project. It is designed to let Alex talk
to a Telegram bot, then have the local agent use Alex's personal LINE on this
Mac to check approved LINE groups, summarize important messages, and save useful
memory into the `alex-mind` Obsidian vault.

### What Is Ready Now

- A local Telegram bot token is saved in `.env`.
- The project knows the bot username: `@AlexmaClone_bot`.
- The clone has a local group watchlist in `config/groups.json`.
- The current local tags are:
  - `BNI`
  - `AI`
  - `family`
  - `Friends`
- Two approved groups are configured locally:
  - BNI group tagged `BNI`
  - AI group tagged `AI`
- The clone can understand many natural-language commands.
- The clone can turn captured LINE messages into a daily report.
- The clone can save raw captures, reports, digests, and send audits into
  `alex-mind`.
- The clone has a policy gate that blocks or asks confirmation before risky
  sends.

### What Is Not Ready Yet

- It does not yet open LINE and read live messages by itself.
- It does not yet click Send in LINE.
- It does not yet run automatically at 09:00, 12:30, or 20:00.
- It does not yet read Google Calendar live.

The current system is the brain and command parser. The next work is the
Computer Use "hands" that operate LINE safely.

### How Alex Will Use It

Alex will message the Telegram bot:

```text
分身，去看 AI 群今天有什麼重要的
```

The intended flow is:

1. Telegram receives Alex's command.
2. Alex Clone parses the command.
3. It sees `AI` means the approved AI LINE group.
4. It opens Alex's personal LINE on this Mac.
5. It checks the group title.
6. It reads new messages since the last checkpoint.
7. It saves the raw messages into `alex-mind`.
8. It creates a summary.
9. It replies to Alex in Telegram.

### Example Commands

```text
掃 AI 群
看 BNI 今天有什麼重要的
整理 Friends 群重點
檢查 family 有沒有需要我回
更新 alex-mind，把今天 AI 群重點存起來
幫我草擬回 AI 群：我晚點整理資料
確認送出
群組列表
```

### Safety Rule

Because V1 uses Alex's personal LINE identity, sending is careful by default.
The clone should verify the active group title and ask confirmation before
sending unless Alex has explicitly allowed that type of message.

## 中文

Alex Clone 是 Alex 的「分身助理」專案。它的用途是讓 Alex 在 Telegram 對分身下指令，然後本機 agent 使用這台 Mac 上 Alex 本人的 LINE，去查看已核准的 LINE 群組、整理重點，並把有價值的記憶寫進 `alex-mind` Obsidian vault。

### 現在已經完成什麼

- Telegram bot token 已經存到本機 `.env`。
- bot 名稱是：`@AlexmaClone_bot`。
- 本機有一份群組 watchlist：`config/groups.json`。
- 目前支援的群組標籤：
  - `BNI`
  - `AI`
  - `family`
  - `Friends`
- 目前本機已核准兩個群組：
  - 一個 BNI 群，標籤是 `BNI`
  - 一個 AI 群，標籤是 `AI`
- 分身可以理解很多自然語言指令。
- 分身可以把已擷取的 LINE 訊息整理成每日報告。
- 分身可以把 raw capture、report、digest、send audit 寫進 `alex-mind`。
- 分身有 policy gate，遇到風險訊息會阻擋或要求 Alex 確認。

### 還沒完成什麼

- 還不能自己打開 LINE 並讀取即時訊息。
- 還不能自己在 LINE 裡按送出。
- 還沒有自動在 09:00、12:30、20:00 執行。
- 還沒有接 Google Calendar。

現在完成的是「大腦與指令理解」。下一步是做「手」：用 Computer Use 安全操作 LINE。

### Alex 會怎麼使用

Alex 傳訊息給 Telegram bot：

```text
分身，去看 AI 群今天有什麼重要的
```

預期流程：

1. Telegram 收到 Alex 的指令。
2. Alex Clone 解析指令。
3. 它知道 `AI` 代表已核准的 AI LINE 群。
4. 它打開這台 Mac 上 Alex 本人的 LINE。
5. 它確認目前群組標題正確。
6. 它讀取上次之後的新訊息。
7. 它把 raw 訊息存進 `alex-mind`。
8. 它產生摘要。
9. 它回 Telegram 給 Alex。

### 指令範例

```text
掃 AI 群
看 BNI 今天有什麼重要的
整理 Friends 群重點
檢查 family 有沒有需要我回
更新 alex-mind，把今天 AI 群重點存起來
幫我草擬回 AI 群：我晚點整理資料
確認送出
群組列表
```

### 安全規則

因為 V1 使用的是 Alex 本人的 LINE 身份，所以送訊息預設要很小心。分身必須先確認目前 LINE 群組標題正確，並且在送出前詢問 Alex，除非 Alex 已經明確允許某類低風險訊息可以自動送出。


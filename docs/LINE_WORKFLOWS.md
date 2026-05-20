# LINE Workflows

## Approved Group Lifecycle

1. Alex adds the clone to a group or authorizes the personal LINE executor.
2. Clone detects or records group name.
3. Alex sets policy:
   - observe only,
   - daily report,
   - draft replies,
   - auto-send approved patterns.
4. Clone starts recording summaries and open loops.
5. Any outgoing message follows the group policy gate.

## Daily Group Report

Each group report should include:

- important messages,
- unanswered questions for Alex,
- tasks and promises,
- relationship signals,
- opportunities,
- suggested replies,
- recommended next action.

## Reply Command Examples

| Alex says | Clone action |
|---|---|
| `幫我回 AI 群，說我明天整理資料` | Draft or send based on policy |
| `總結今天 AI 群發生什麼` | Summarize recent group context |
| `把這個人加入追蹤` | Update people note and open loops |
| `今晚幫我回覆所有低風險訊息` | Process allowlisted replies, ask on ambiguous ones |

## LINE Executor Notes

Use clipboard paste for multi-line messages. Do not type multi-line content
character-by-character because LINE for Mac treats Return as send.


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

## Follow-Up Tags

Each watched LINE group can carry one or more follow-up tags so the clone knows
which mental lane to use when reporting, prioritizing, and writing vault notes.

Initial tags:

| Tag | Meaning |
|---|---|
| `BNI` | BNI chapter, referrals, PALMS, meeting, leadership, member follow-up |
| `AI` | AI community, tools, AI news, agent projects, learning material |
| `family` | Family logistics and personal care context |
| `Friends` | Friends, social plans, casual follow-up |

The real watchlist is stored locally in `config/groups.json` and ignored by
Git. The public `config/groups.example.json` only shows the schema.

## Access Model

V1 primary route is Computer Use with Alex's personal LINE session already
logged in on this Mac. The clone operates the same LINE identity Alex uses, so
it must be more careful than a separate bot account:

- open the LINE desktop/web UI already authenticated on this PC,
- search/select only an approved group,
- verify the active group title before reading or sending,
- use clipboard paste for composed messages,
- ask Alex before sending anything outside allowlisted low-risk patterns,
- take screenshots when stuck and for important send proof,
- write an audit record for every outbound message.

Optional later route is the LINE Messaging API with a clone LINE Official
Account:

- enable `Allow bot to join group chats`,
- invite the clone OA into an approved group,
- store `source.groupId` from webhook events as the stable group key,
- use push messages to send to that group only when policy allows.

API mode is useful only when Alex wants a separate clone account and a group can
accept that account.

Official references:

- <https://developers.line.biz/en/docs/messaging-api/group-chats>
- <https://developers.line.biz/en/docs/messaging-api/sending-messages/>

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

When sending via Computer Use, the executor must verify the active group name
before pasting or sending. When sending via API, group push messages use the
group ID as the `to` target.

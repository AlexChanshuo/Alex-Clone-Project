# Operating Policy

## Group Access

The clone can operate only in groups that Alex explicitly approves. Approval
should record:

- group display name,
- group id or stable identifier if available,
- allowed actions,
- whether replies are draft-only or auto-send,
- reporting cadence,
- retention rules.

## Reply Policy

| Situation | Behavior |
|---|---|
| New group | Observe/report only until Alex approves reply mode |
| Direct command from Alex | Execute within the command scope |
| Low-risk routine reply | Auto-send only if group policy allows it |
| Ambiguous or emotional message | Draft and ask Alex |
| Commitment involving time/money | Check calendar/context and ask Alex |
| Sensitive personal info | Ask before sending or moving across contexts |

## Identity

The clone should be transparent when needed. For test broadcasts and automation
rollouts, include wording like:

> 正在測試 Alex 分身 Agent

For normal private productivity, the wording depends on group policy and Alex's
preference.

## Audit

Every send should write:

- timestamp,
- target group,
- source command,
- message hash,
- whether confirmation was required,
- screenshot or delivery proof path when available.


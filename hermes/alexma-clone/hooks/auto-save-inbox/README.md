# Auto Save Inbox Hook

Hermes supports lifecycle hooks. AlexMind's existing architecture uses an
`agent:start` hook to deterministically save every Telegram message before the
LLM replies.

For Alexma Clone, use the same principle:

1. Telegram message arrives.
2. Hook saves the raw message into `alex-mind/raw/inbox/alexma-clone/`.
3. Hermes LLM responds and may call Alex Clone CLI skills.

The exact hook registration depends on the installed Hermes version/config.
Keep deterministic capture in Python or shell, not in LLM instructions.


# Calendar Workflows

## Google Calendar Jobs

After Alex connects Google Calendar, the clone should:

- read today's and tomorrow's schedule,
- detect conflicts before Alex commits to plans,
- include calendar-aware reminders in daily reports,
- suggest reply wording when schedule affects availability,
- ask before creating or editing events.

## Examples

| Situation | Behavior |
|---|---|
| Someone asks Alex for a meeting | Check free/busy, draft available windows |
| Group announces event | Add to "possible events" list, ask before calendar write |
| Alex says `幫我排進去` | Prepare event details, ask before final create |
| Tomorrow is crowded | Morning report warns Alex and suggests response triage |


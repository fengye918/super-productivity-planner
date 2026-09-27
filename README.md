# Super Productivity Planner

A small personal planning repository.

## What matters
- `schedule.ics` — calendar feed subscribed to by Super Productivity.
- `planner_events.ics` — ChatGPT-managed weekly planning events; automatically merged into `schedule.ics`.
- `PLANNER_RULES.md` — stable scheduling rules shared across conversations.
- `ACTIVE_CONTEXT.md` — current priorities and completion state.
- `data/zju_todos.json` — raw normalized 学在浙大 todo mirror.
- `course_materials/` — downloaded homework/course material and categorized solution PDFs.

## Cross-chat command
Discuss first. When the plan is agreed, say:

> **落到日程**

Then the agreed **current-week** plan may be written to the calendar.

## Automation
- 学在浙大 sync runs automatically several times per day.
- Course solution PDFs rebuild automatically when their LaTeX source changes.
- Planner events automatically merge into the published calendar feed.

Credentials are stored only as GitHub Actions secrets; never place passwords/cookies in repository files.

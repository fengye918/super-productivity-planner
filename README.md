# Super Productivity Planner

This repository is the source behind the Super Productivity schedule.

- `schedule.ics`: calendar feed published through GitHub Pages and subscribed to by Super Productivity.
- `PLANNER_RULES.md`: shared planning rules used across ChatGPT conversations.
- `data/zju_todos.json`: normalized current 学在浙大 assignments.
- `data/zju_changes.json`: newly added, changed, or removed assignments from the most recent sync.
- `scripts/fetch-zju.mjs`: fetches 学在浙大 todo data and a compact assignment-detail excerpt.
- `.github/workflows/sync-zju.yml`: scheduled synchronization workflow.

## Cross-chat command

After discussing a plan in any ChatGPT conversation, say:

> **落到日程**

That phrase authorizes the assistant to read `PLANNER_RULES.md`, reconcile the proposal with the existing `schedule.ics`, and write the agreed changes.

## One-time 学在浙大 setup

The repository deliberately contains **no Zhejiang University credentials**.

In GitHub open:

`Settings → Secrets and variables → Actions → New repository secret`

Create exactly these two secrets:

- `ZJU_USERNAME`
- `ZJU_PASSWORD`

Then open:

`Actions → Sync 学在浙大 → Run workflow`

After the first successful run, the workflow runs automatically four times per day (Asia/Shanghai approximately 08:15, 12:45, 18:15, 22:15).

Do not place account passwords, session cookies, or `.env` files in this public repository.

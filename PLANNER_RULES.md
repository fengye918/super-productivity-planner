# Planner Rules

## Schedule
- Time zone: `Asia/Shanghai`.
- Normal earliest work start: **08:00**; public holidays: **08:30**.
- Latest planned work end: **22:30**.
- Prefer **19:00-22:00** as a normal work window.
- Weekends are treated like weekdays unless the user says otherwise.
- Fixed classes/exams are hard constraints; avoid overlaps and keep transition buffer.
- Keep at least **3 hours/day** for meals, entertainment and recovery.
- Keep **one additional unscheduled hour/day** for English practice; routine English is not written into Schedule by default.

## Authorization and horizon
- Before the user says **“落到日程”** / **“落实日程”**: discuss and negotiate only.
- After that phrase: write the agreed plan to `schedule.ics`.
- By default, only write events inside the **current Monday-Sunday week**.
- Future-week blocks are allowed only when a major assignment/project cannot reasonably finish otherwise.

## Homework and course catch-up
- User-confirmed completion/submission **overrides** stale 学在浙大 todo state. Do not reschedule a task the user says is finished.
- Ordinary homework: **max 2.5 h total per assignment** unless renegotiated.
- Dedicated catch-up/reinforcement: **about 2 h max per course per week** by default.
- Prefer concise, execution-oriented blocks over long planning sessions.

## Exams
- Every known exam gets dedicated review time.
- Review titles must name specific content, not just “复习”.
- With past papers, calibrate: topic weight, recurring question types, standard procedures, timing and common traps.
- Default progression: knowledge map/formulas → topic problems → timed paper → error repair → final recall sheet.

## Major assignments / open-ended projects
- Spend roughly **30-40%** of expected effort on requirements, framing, architecture, alternatives, innovation design and feasibility checking before full implementation.
- Innovation should be meaningful, testable and tied to a clear benefit; do not force novelty for novelty’s sake.
- Use milestone outputs: requirements → design/innovation → feasibility → implementation/experiment → draft → revision → final.

## Research
- Research blocks must name a concrete output/evidence, not vague “do research”.
- Prefer end-to-end evidence: working chain, reproducible baseline, curve, experiment note, validated interface, etc.

## Course materials and solutions
- Automatically retrieved course/homework material may be stored in this repo.
- Formal solution PDFs are stored by course:
  - `course_materials/<课程>/solutions/<作业>_标准解答.pdf`
  - editable source under `course_materials/<课程>/solutions/source/`
- Keep `course_materials/README.md` as the cross-course index.
- Formal solution style: standard exam-answer format, clear derivation, numbered subproblems, concise reasoning, final answers clearly marked.

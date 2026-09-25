# Planner Rules

- Time zone: Asia/Shanghai
- Earliest planned work start: 08:00
- Latest planned work end: 22:30
- Keep at least 3 hours each day for meals, entertainment, and recovery.
- Treat weekends like weekdays unless the user explicitly says otherwise.
- Fixed classes and exams are hard constraints.
- Avoid overlaps and keep realistic buffer time.
- English is primarily a Habit, not a fixed 08:00 schedule block.

## Short command
The exact phrase **落到日程** authorizes updating `schedule.ics` using the plan agreed in the current conversation.
Before that phrase, analyze and negotiate only.

## Homework
- Automatically synced 学在浙大 data may be used as input, but sync alone never authorizes calendar changes.
- Analyze assignment content and available course material first, estimate effort, then propose concrete work blocks.
- Finish substantive work before the deadline and keep a submission/review buffer when practical.
- Long assignments and projects must be decomposed into milestone blocks with a concrete output for each block.
- Prefer long uninterrupted blocks for substantial work.

## Research
- Research blocks must name a concrete output/evidence.
- Cephalo-Ring and underwater MARL should both keep progressing, with weekly weight adjusted to current state and deadlines.

## Course documents and solution PDFs

- Course documents and homework attachments may be stored publicly in this repository when useful for automated planning.
- Prefer automatic retrieval over asking the user to upload files manually.
- For each captured homework, use the assignment statement plus relevant course PPT/PDF material when available.
- Before scheduling, produce a short analysis of scope, difficulty, likely solution path, and a realistic time estimate.
- For problem-set style homework, generate a polished solution PDF when requested or when it materially helps execution.
- The solution PDF should read like a formal exam answer: clear derivation, standard notation, necessary formulas, concise reasoning, numbered subproblems, final answers clearly marked, and no conversational filler.
- If a source document is incomplete or unavailable, state that limitation rather than inventing requirements.

## Major assignments and innovation

- For major assignments, reports, course projects, and design work, allocate extra time to the **problem framing / architecture / preliminary design** stage before implementation.
- The early stage should explicitly consider: task requirements, grading criteria, constraints, alternative approaches, technical risk, available course material, and where a defensible element of originality can be introduced.
- Do not force novelty for its own sake. Prefer small but meaningful innovation that is technically justified, testable, and compatible with the assignment requirements.
- When several approaches are plausible, compare them before committing and reserve time for a short feasibility check or prototype.
- For major deliverables, the default milestone order is:
  1. understand requirements and grading target;
  2. collect relevant PPT/PDF/material;
  3. design the approach and identify possible innovation;
  4. feasibility check / prototype;
  5. implementation / derivation / experiment;
  6. draft;
  7. revision and validation;
  8. final submission.
- Planning should deliberately give stages 1-4 enough uninterrupted time; they are not treated as a quick preface to the "real work".
- Default allocation for a substantial open-ended assignment: roughly **30–40% of the estimated total effort** goes to requirements analysis, framing, architecture, alternative comparison, innovation design, and a feasibility check before committing to the main implementation. Adjust only when the rubric or deadline clearly calls for a different split.
- Innovation should be tied to an explicit benefit (better performance, clearer methodology, stronger evidence, lower complexity, better robustness, or a more insightful comparison) and should have a way to verify whether it actually helped.

## Weekly scheduling horizon

- When the user authorizes **落到日程**, only create or modify Schedule blocks inside the **current Monday-Sunday calendar week** by default.
- Do not pre-fill future weeks merely because there is free space.
- Exception: a major assignment / course project / report may receive preparatory blocks in a later week only when the current estimate shows that restricting work to the current week would make timely completion unrealistic, or when the task has long-lead dependencies.
- A deadline or exam in a future week may still justify review/preparation blocks **inside the current week**; the horizon rule restricts the dates being written, not the planning awareness.

## Exam review

- Every known exam must receive dedicated review time before the exam.
- Review blocks must be content-specific, not generic titles such as “复习考试”.
- When past papers are available, use them to calibrate topic weights, recurring question types, standard solution procedures, time pressure, and common traps.
- Default review progression:
  1. rebuild the tested knowledge map and formula/definition checklist;
  2. representative problems by topic;
  3. timed past-paper or mock-paper practice;
  4. error classification and targeted patching;
  5. final concise recall sheet / high-frequency procedures.
- If an exam is within the next 14 days, the current week's plan should normally include at least one exam-oriented review block unless the user explicitly deprioritizes it.

## Daily English reserve

- Keep a preferred **1-hour English development block per day** when schedule capacity allows.
- This is separate from the user's English Habit: the Habit keeps continuity, while the one-hour block is for deliberate practice such as technical listening, project speaking, terminology output, writing/translation, or CET-6 weakness repair.
- English time is movable within the day and should not displace urgent deadlines or critical experiments.

## Holidays

- On public holidays, the earliest planned work start is **08:30** instead of 08:00.
- Holiday mornings should default to lighter, lower-friction work unless the user explicitly asks for an intensive block.
- Preserve additional rest space on holidays rather than using the later start merely to compress the same workload.


## Daily unscheduled reserve

- Do **not** put routine English practice on the Schedule by default.
- In addition to the existing requirement to keep at least 3 hours for meals, entertainment, and recovery, leave **one extra hour unscheduled each day** so the user can use it for English practice.
- This English reserve is protected free capacity, not a calendar event, unless the user explicitly asks to schedule English.


## Homework time cap

- For ordinary course homework, schedule **no more than 2.5 hours total per assignment** by default.
- Keep homework analysis concise and execution-oriented; do not spend a large fraction of the budget on planning.
- If the available evidence strongly suggests an assignment cannot be completed responsibly within 2.5 hours, do not silently exceed the cap; tell the user and renegotiate.

## Evening work preference

- Prefer using **19:00-22:00** as a normal task window on most days.
- Do not leave large portions of the evening empty by default; place suitable coursework, review, planning, or research there.
- Keep the user's protected meal/recovery time and the extra unscheduled English hour elsewhere in the day when practical.
- On holidays, keep the morning light, but the evening may still contain normal work blocks unless the user asks for a fully relaxed holiday.

## Weekly course catch-up cap

- For a course that needs catch-up/reinforcement because lectures were not fully absorbed, schedule **no more than about 2 hours of dedicated catch-up per course per week** by default.
- Prefer one focused 90-120 minute reconstruction block over several scattered review blocks.
- Ordinary homework time is tracked separately under the homework cap; do not inflate catch-up time by relabeling homework as review.
- If a course genuinely needs more than 2 hours of catch-up in a week, explain why and renegotiate before adding more.

## Solution repository organization

- Generated homework solution PDFs should be stored directly in this GitHub repository by course, not left only as chat attachments.
- Canonical layout:
  - `course_materials/<课程名>/solutions/<作业名>_标准解答.pdf`
  - editable LaTeX/source files go under `course_materials/<课程名>/solutions/source/`
  - optional first-page visual QA previews go under `course_materials/<课程名>/solutions/preview/`
- Maintain `course_materials/README.md` as the cross-course solution index.
- When a new formal homework solution is generated, update the corresponding course folder and the index automatically unless the user explicitly asks otherwise.

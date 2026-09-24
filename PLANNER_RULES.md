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

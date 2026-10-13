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

## Weekly RoboCup and active robotics research
- Every week reserve **at least one focused RoboCup project implementation/experiment block (default 2 hours)** before the Saturday 19:30 regular meeting. Preferred fixed block is **Friday 16:30-18:30**, with a recurring calendar event starting 2026-10-16. If a Friday conflict occurs, move that week's work earlier rather than dropping it. RoboCup meeting itself does not count as project work.
- When Qizhen and MARL research are active, prioritize concrete research deliverables in remaining open deep-work windows before optional general-interest learning; preserve hard classes, due work, English buffer and at least three hours daily for eating, recovery, and recreation.
- For Qizhen, track **CFD / physical flow-field validation** and **MA735 closed-loop servo angular-speed chain** as two independently testable workstreams. Workstreams should each leave a reproducible numerical case, measurement, code test or clear blocker. Never schedule electrical power-on of an incomplete MA735 PCB.
- Short high-efficiency learning blocks: check actual lecture material, recall without notes, solve a representative problem independently, verify using course source, record an actionable error or next step. Reserve sufficient lecture-to-lecture comprehension time instead of counting passive reading as mastery.

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

## Personal development exploration
- Reserve about **1 hour every week** for deliberate exploration of the user's longer-term study/research/career direction.
- This should be a real Schedule block by default, not merely hidden free time.
- The block is for open exploration rather than immediate deliverables: new robotics directions, research questions, tools, technical trends, or possible future project areas.
- Keep it lightweight and curiosity-driven; do not let it crowd out urgent coursework or active project milestones.

## Interest learning
- When the week still has genuine spare capacity after fixed courses, deadlines, current research priorities, rest, and the protected English hour, optional blocks may be used for personal-interest learning.
- Current interest areas include:
  - **智能语音 / voice assistant project**
  - **网络层学习**
- Interest blocks should stay optional and should preferably produce a small concrete result (prototype, note, experiment, or concept map) rather than passive browsing.

## Modern Control Theory review
- Every **Modern Control Theory class actually attended** should receive a separate **1.5-hour post-class review/understanding block**.
- Do not merge that review block into homework time. Homework and post-class understanding are separate purposes.
- Preferred review flow: closed-book knowledge skeleton -> check PPT/notes -> hand-derive key formulas -> 1 representative problem -> remaining-gap list.
- If a Modern Control class is explicitly skipped/cancelled, do not create a post-class review block for that class.

# Planner Rules

## Schedule
- Time zone: `Asia/Shanghai`.
- Normal earliest work start: **08:00**; public holidays: **08:30**.
- Latest planned work end: **22:30**.
- For an explicitly requested pre-deadline sprint, evenings on non-travel-eve days may extend to **23:00** if the user asks; keep this an exception, not a default. Preserve meals/recovery, and on the night before an early flight stop by 22:00 (preferably earlier). No work inside an explicit travel blackout.
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
- User-confirmed ZJU rule (2026-10-26): when an item disappears from 学在浙大's synced pending-homework list, treat it as **successfully submitted**. Remove redundant homework/submission reminders; no extra receipt verification is needed. This applies to 学在浙大 homework only, and explicit user updates take priority.
- Ordinary homework: **max 2.5 h total per assignment** unless renegotiated.
- Dedicated catch-up/reinforcement: **about 2 h max per course per week** by default.
- Prefer concise, execution-oriented blocks over long planning sessions.

## Protection of targeted course review
- When the user reports missed or poorly understood course content, schedule a concrete 60-90 minute catch-up **before their next attended class** of that course, grounded in the actual lecture PPTs and finished by doing representative problems and correction notes. Do not automatically sacrifice these sessions when increasing project time.
- User-confirmed full completion of a review or assignment means no duplicate future time block. An explicitly suppressed assignment is excluded from future scheduling even if the LMS still shows a todo; do not falsely mark a suppressed item as submitted.

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
- For active SSL control or hardware responsibility, target **3.5-5 hours/week** of personal implementation and evidence-based validation in ordinary weeks: preferably a 1.5-hour midweek block plus the protected 2-hour Friday block. A weekly meeting is coordination, not engineering delivery. On travel weeks, rearrange work before departure and report asynchronously rather than work during declared blackout dates; do not fill hours with aimless browsing.
- Every week reserve **at least one focused RoboCup project implementation/experiment block (default 2 hours)** before the Saturday 19:30 regular meeting. Preferred fixed block is **Friday 16:30-18:30**, with a recurring calendar event starting 2026-10-16. If a Friday conflict occurs, move that week's work earlier rather than dropping it. RoboCup meeting itself does not count as project work.
- When Qizhen and MARL research are active, prioritize concrete research deliverables in remaining open deep-work windows before optional general-interest learning; preserve hard classes, due work, English buffer and at least three hours daily for eating, recovery, and recreation.
- For Qizhen, track **CFD / physical flow-field validation** and **MA735 closed-loop servo angular-speed chain** as two independently testable workstreams. Workstreams should each leave a reproducible numerical case, measurement, code test or clear blocker. Never schedule electrical power-on of an incomplete MA735 PCB.
- Short high-efficiency learning blocks: check actual lecture material, recall without notes, solve a representative problem independently, verify using course source, record an actionable error or next step. Reserve sufficient lecture-to-lecture comprehension time instead of counting passive reading as mastery.

## Declared travel blackout
- When the user explicitly blocks travel dates, treat the entire inclusive date range as **no academic/research/project work** and create an all-day absence block; move existing optional work before departure or after return.
- Do not delete official class source records or cancel team-wide meetings: hide only the user's conflicting imported class occurrences and use recurrence exceptions for their personal standing meetings. Record any genuine missed-class catch-up before the next attended session.
- Never infer flight airport, return flight clock time or ground transportation departure without explicit evidence. Reserve reasonable packing and transit preparation, plus sleep before early flights.

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


## 学在浙大同步与标准解答（长期默认）
- 传感与检测等课程的最新课件若在末页布置“作业/讨论”，即使独立的学在浙大待办列表没有列出，也应从当期课程官方 material 活动读取原始幻灯片，严格区分明确“作业”和“讨论”，只依据确切的 PPT 内容撰写、计算与核验参考解答，不可用旧版文档代替最新版本。
- 用户明确要求：**以后每次检查或更新学在浙大作业时，同步处理适合解题的新增作业的标准参考答案 PDF**；不要只更新待办或日程。优先从课程平台同步到 `course_materials/<课程>/homework/` 的真实附件逐题读取，再求解、独立核算数值/符号、生成可编辑 TeX 和完整 PDF、渲染检查，并归档 `course_materials/<课程>/solutions/source/` 及 `solutions/`，更新 `course_materials/README.md`。
- 若新增任务是**上传成绩证明、实机实验、在线提交、团队协作等非传统解题任务**，不能编造“标准答案”。应提供提交检查表、实验方案或可复现参考脚本；未实测或未经平台提交的状态不得伪称完成。
- 学在浙大系统待办状态可能滞后，永远以用户确认的**已完成、已提交或不再排程**为优先。对新作业核对截止时间、是否需要做题、现有日程有无空档，普通作业默认不超过 2.5 小时；在指定截止前完成和自检。
- 不要声称已自动后台生成；若需在对话之外定时检查与通知，必须由有效的计划任务或仓库自动流程支持。

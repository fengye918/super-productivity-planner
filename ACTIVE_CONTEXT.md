# Active Planning Context

Updated: 2026-09-24

This file records current short-horizon priorities. It is context for planning, not authorization to change `schedule.ics`.

## Current-week special priorities

### Qizhen / Cephalo-side project
- Start printing the needed 3D-printed parts; preferably start the print in the afternoon. This only needs a short reminder block rather than reserving the entire print duration.
- Watch the motion-capture system operation/training videos and produce concise operating notes.
- Study how to place suitable markers on the undulating fin so that the motion-capture system can robustly reconstruct the fin's relevant angles.
- Marker work should consider: visibility/occlusion, marker identity, rigid vs deforming geometry, number/placement of points, angle reconstruction definition, coordinate frames, calibration, and whether the measurement survives fin oscillation without markers detaching or disturbing motion.

### Underwater MARL
- Reserve one substantial deep-work block for the user to design a complete MARL scenario independently.
- A complete scenario should at least pin down: task/problem statement, agents, observations, actions, dynamics/environment, reward, termination, centralized-training information, decentralized-execution information, metrics, baselines, and the first experiment that could falsify a bad design.

### English
- Prefer to reserve 1 hour per day for deliberate English practice, in addition to the existing Habit.

### Modern Control Theory
- Needs dedicated catch-up/reinforcement because recent lectures were not absorbed well.
- Use reconstruction review rather than passive rereading: recent PPT/notes -> concept map -> key derivations -> representative problems -> error list.
- Until exact PPT content is synced, do not invent chapter-specific review topics.

### Artificial Intelligence and Machine Learning
- Needs dedicated reinforcement.
- Current known homework topic is linear models, especially Ridge/Lasso, regularization strength, feature selection, standardization, and method choice.
- Review should combine concept reconstruction, objective-function/geometry intuition, answering the current questions without notes, and at least one small concrete example or experiment.

### Big Data Analytics and Application Introduction — major assignment exploration
Teacher-provided assignment requirements visible in the supplied slide:
- Prefer an industrial-domain problem; use an open competition dataset or teacher-provided data when permitted.
- Deliverables: demo slides (about 20+ pages), a Word-format written report, source code, and dataset.
- Introduce the topic/problem and data source with links.
- Analyze the problem, analyze results, and provide the team's own interpretation; identifying problems and proposing new ideas is encouraged.
- Report should state leader, members, division of work, and contributions.
- Demo is held about two weeks before the end of the course.

Current direction is immature but the user is interested in a **zero-shot / semantic** angle.
Planning principle:
- Treat this as a low-priority exploration/filler block when higher-priority coursework and research are under control.
- First explore the problem/data pair and what “zero-shot / semantic” means operationally before choosing a model.
- A promising class of directions to investigate is industrial fault/anomaly analysis where fault classes or operating conditions have meaningful semantic descriptions, so an ordinary supervised baseline can be compared with a semantic or unseen-class generalization extension.
- Do not commit to novelty before checking dataset suitability and whether the claim can be tested cleanly.

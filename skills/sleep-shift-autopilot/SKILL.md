---
name: sleep-shift-autopilot
description: "Autonomous overnight & away-from-keyboard execution workflow. Trigger immediately whenever the user says they are going to sleep ('我睡觉了', '去睡了', '先睡了', '睡醒汇报', 'going to sleep') alongside pre-sleep requests. Enforces: zero blocking questions while the user sleeps, immediate execution of all unambiguous tasks, deferral of genuine product/destructive forks to a morning sign-off section, proactive execution of 2-3 self-assigned style-aligned polish & delight tasks after assigned work completes, full technical + visual verification, clean Git commits, and a structured morning wake-up report."
---

# Sleep-Shift Autopilot (`我睡觉了` 夜间全自动执行协议)

When the user says they are going to sleep and leaves instructions, the single worst failure mode is **pausing to ask clarifying questions before acting**, wasting 8 hours of idle runtime. This skill flips the agent into **Autonomous Night-Shift Delivery Mode**.

---

## 1. Prime Directive While the User Sleeps

1. **NEVER stop to ask questions before working.** If a user is asleep, an unanswered question stalls all progress until morning.
2. **Triage immediately** upon reading the pre-sleep prompt:
   - **Track A — Clear & Reversible Tasks (Execute 100% Now):** Anything explicitly requested or strongly implied by the codebase, established aesthetic, and safety rules. Resolve minor ambiguities by choosing the option that best aligns with the project's documented style, past user feedback, and safest reversibility.
   - **Track B — Genuine High-Risk / Irreversible Product Forks (Defer to Morning Ritual):** Destructive schema wipes, paid external deployments, or purely subjective fork decisions that were *not* hinted at. Log them cleanly under **"睡醒开工仪式待拍板项"** at the end of the final morning report—never block Track A for them.
3. **Budget Sleep Time Into Two Waves:**
   - **Wave 1 (User's Explicit Requests):** Complete every item the user asked for before sleeping, down to real-world verification.
   - **Wave 2 (Self-Assigned Polish & Delight Tasks — Mandatory):** Once Wave 1 is verified, proactively invent and complete **2–3 high-taste optimizations, atmosphere upgrades, UX/motion micro-refinements, or easter eggs** strictly faithful to the user's established aesthetic (e.g., Old Money architectural craft + Apple fluid minimalism). Think like an obsessed art director & principal engineer using the extra overnight runway wisely.

---

## 2. Overnight Execution Loop

1. **Inspect First, Plan Tightly:** Read only the directly impacted files, confirm repo red lines (`AGENTS.md`, asset size caps, security, style rules), and lock an execution plan.
2. **Batch & Delegate Heavy Work:** Combine parallel file reads/edits and delegate parallel heavy texture/3D/math/copy generation (e.g., via `deepseek-collab` when available) so main-agent reasoning stays crisp.
3. **Verify Against Ground Truth:**
   - Run static checks (`node --check`, forbidden-word/CDN/env checks, file-size assertions).
   - Run real headless browser QA across desktop & tablet viewports (`0` console errors, `0` HTTP `>=400`, `0` HUD overlaps).
   - **Visually inspect actual screenshots** before calling anything done. Fix any visual flaw immediately while the user still sleeps.
4. **Commit Cleanly & Leave Zero Stale Daemons/Temp Files:**
   - Commit cohesive, working milestones (never leave half-broken files in the working tree).

---

## 3. Morning Wake-Up Briefing Format

When finished, present a warm, scannable report using [references/morning-report-template.md](references/morning-report-template.md) containing:
1. **已全部落地的睡前任务** (each user request with exact file/visual result),
2. **自主加餐完成的润色与惊喜功能** (the 2–3 self-assigned Wave 2 upgrades),
3. **实机验收结果** (viewports tested, static/runtime pass status, visual notes),
4. **睡醒开工仪式 · 可选拍板项** (concise 1–3 optional creative directions for the next daytime session, clearly formatted for quick thumbs-up/down).

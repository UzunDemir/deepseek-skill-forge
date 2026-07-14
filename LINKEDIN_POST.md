---
# LinkedIn Post — copy this text directly to LinkedIn
# Author: [Your Name]
# Date: 2026-07-14
---

We just turned 172 OpenAI Codex subagents into native DeepSeek TUI skills — and made them better in the process.

Here's why this matters ⬇️

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Most AI coding assistants give you ONE agent. One context. One shot.

But real engineering work isn't monolithic:

• Bug fix needs backend expertise + security review + codebase search
• PR review needs correctness checks + docs verification + pattern analysis
• New feature needs fullstack implementation + testing + API alignment

You need specialists, not generalists.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What we built:

74 SKILL.md files — specialized instructions for DeepSeek TUI
    ↓ loaded into main agent context automatically
    ↓ each has: working mode, focus areas, quality checks, return contract
    ↓ covers: Python, Rust, Go, K8s, Terraform, security, ML, LLMs and more

98 spawn templates — ready-to-use prompts for parallel sub-agents
    ↓ spawned via agent_spawn for concurrent review/investigation
    ↓ includes: security-auditor, reviewer, docs-researcher, search-specialist

4 orchestration presets — composition workflows
    ↓ pr-review-chain: parallel review + docs + search
    ↓ bug-investigation: trace → debug → fix → audit
    ↓ feature-implementation, repo-exploration

172 automated validations — 0 errors, 0 warnings

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Key difference from original Codex approach:

• Codex: one big sub-agent per task
• Ours: skill (I do it) + spawn templates (I parallelize it)
          + orchestration presets (I compose it)

This gives us structured, repeatable, FAANG-level quality on every interaction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Practical example:

User: "POST /api/payments/retry is 500ing in prod"

Without skills → "fixed it, tests pass"
With backend-developer skill → structured response:
  • Files changed (+8/-3)
  • Behavior: added state validation before retry
  • Validataion: success path + failure path
  • Residual risk: missing idempotency check

Every. Single. Time.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next steps:
→ Convert more agent definitions (we have ~150 more candidates)
→ Add CI pipeline with automated benchmark harness
→ Build runtime feedback loop (capture real usage → improve skills)

Full project (MIT): link in comments or DM me.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Have you specialized your AI coding agents? Or do you keep one generalist?

I'd love to hear what works for your team.

#AI #DeepSeek #SoftwareEngineering #LLM #DeveloperTools #AIEngineering #OpenSource

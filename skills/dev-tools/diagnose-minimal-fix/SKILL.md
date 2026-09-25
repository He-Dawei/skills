---
name: diagnose-minimal-fix
description: "Escalate an unresolved or repeated error after an attempted fix, or when debugging has stalled and a clear status or handoff is needed. Use after a repair attempt fails, the same bug recurs, or new evidence invalidates the current diagnosis. Restate the latest error, update the impact map and ranked causes, select the next smallest evidence-backed change, and define verification. Do not use for an initial straightforward bug; use debugging-methodology first."
---

# Diagnose Minimal Fix

Recover discipline when a repair attempt fails or debugging stalls. This skill owns escalation and handoff; `debugging-methodology` owns the initial five-step diagnosis.

## Required Sequence

1. **Restate the current error.** Capture the latest exact error, the command or action that produced it, expected versus actual behavior, and whether it differs from the original failure. List attempted fixes and their observable results.
2. **Update the impact map.** Identify affected entry points, components, users, data, environments, and downstream behavior. Separate confirmed impact from suspected impact and state what remains unaffected.
3. **Re-rank possible causes.** Use the failed attempts as evidence. Mark hypotheses as supported, weakened, or ruled out; add new causes only when the latest result justifies them. Distinguish the root cause from secondary errors introduced during debugging.
4. **Choose the next minimum modification.** Prefer the smallest diagnostic probe or causal edit that separates the leading hypotheses. Preserve public interfaces and data structures. Avoid opportunistic refactors, dependency upgrades, formatting churn, and broad configuration changes.
5. **Define and run verification.** Reproduce the latest failure before editing when possible. After an authorized change, rerun the exact failing case, the original user scenario, and the smallest adjacent compatibility check. State remaining uncertainty and a rollback path when risk warrants it.

If local evidence cannot safely choose among materially different repairs, stop editing and request the missing artifact, access, or user decision.

## Required Status Update

Report in this order:

1. `当前错误`
2. `影响范围`
3. `可能原因（按证据排序，注明已排除项）`
4. `最小修改路径`
5. `验证方法`

Keep the update self-contained so another agent or the user can continue without reconstructing the debugging history.

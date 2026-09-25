---
name: review-task-changes
description: Review completed implementation or configuration work before final delivery. Use after any task that changes code, configuration, schemas, data, or files, especially to check whether edits exceeded the requested scope, touched unrelated files, broke API or data compatibility, missed failure states, or introduced duplicate maintenance logic.
---

# Review Task Changes

Perform a final, evidence-based review of the changes made in the current task. Keep the review limited to the user's requested outcome and the agent's own edits.

## Workflow

1. Reconstruct the contract from the user's request, stated acceptance criteria, and explicitly authorized targets.
2. Collect change evidence. Prefer version-control status and diffs; otherwise enumerate files created, edited, moved, or deleted during the task.
3. Review every item below and mark it `pass`, `issue`, or `uncertain`, with concrete evidence:
   - Scope: Did any behavior or edit exceed the requested work?
   - File boundary: Was any unrelated or user-owned file changed?
   - Compatibility: Are public interfaces, commands, configuration keys, schemas, serialized data, and existing callers still compatible?
   - Failure states: Are realistic invalid inputs, partial failures, missing dependencies, and cleanup or rollback paths handled in proportion to risk?
   - Maintainability: Did the change add duplicate branches, repeated constants, or parallel logic that future maintainers must keep synchronized?
4. Fix a confirmed defect caused by the current task when the correction is safe and remains inside the original scope. Re-run the relevant verification after fixing it.
5. Do not edit unrelated files merely to make the review clean. Report any uncertainty that requires external information or new authority.

## Delivery

Report actionable findings first, ordered by severity, and identify the affected file or component. If all five checks pass, state that concisely and include the verification performed. Do not manufacture findings to fill the checklist.

---
name: post-task-review
description: After every task completion — run a 5-point self-review before declaring done. Scope creep, unintended file changes, API/data compatibility, error handling gaps, and duplicate logic. Trigger automatically after any non-trivial implementation task, file edit, or code change.
---

# Post-Task Self-Review

After every task, before declaring "done," run this 5-point review. Each check must pass or have a documented reason for skipping.

## The Five Checks

### 1. Scope Boundary — Did changes exceed what was asked?

Compare the final diff against the original request. If you touched files or functions outside the stated scope, ask: was it necessary or was it scope creep?

- Count files modified vs. files that should have been modified
- For each extra file: write one sentence justifying why it was needed
- If no justification exists, revert it

### 2. Unintended Targets — Any files changed that shouldn't have been?

Scan the full file list in the diff. Flag any file that was not mentioned in the task description and does not have a direct dependency relationship to the task.

Common offenders: config files, lockfiles, formatting changes in unrelated files, IDE auto-save artifacts.

### 3. Interface & Data Compatibility — Will existing consumers break?

For every function signature, API endpoint, data structure, or config key that changed:
- If it's a public interface: did callers get updated?
- If it's a data format: is the old format still readable? If not, is there a migration path?
- If it's a config: does the default value preserve existing behavior?

### 4. Error & Edge State Handling — What happens when things go wrong?

For each new code path:
- What happens on null/empty/missing input?
- What happens on network timeout or partial response?
- What happens on permission denied or file-not-found?
- Is the error message actionable for the user or just "something went wrong"?

### 5. Duplicate Logic — Did you create maintenance debt?

Search for similar patterns in the codebase before writing new ones:
- Does a utility function already do this?
- Could this be a parameterized call instead of a copy-paste?
- Will someone need to update two places when the logic changes?

If you find existing similar logic that you didn't reuse, fix it now — don't leave it for later.

## Output Format

After completing a task, output a brief review block:

```
## Post-Task Review
1. Scope: [PASS/FAIL] — [1-sentence note]
2. Unintended files: [PASS/FAIL] — [1-sentence note]
3. Compatibility: [PASS/FAIL] — [1-sentence note]
4. Error handling: [PASS/FAIL] — [1-sentence note]
5. Duplication: [PASS/FAIL] — [1-sentence note]
```

If any check FAILs, fix it before declaring the task done. Do not defer — the review is part of the task, not an afterthought.

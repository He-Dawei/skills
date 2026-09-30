---
name: user-execution-guardrails
description: Apply the user's first-principles execution rules to coding, debugging, configuration, cleanup, and other tasks with meaningful side effects.
---

# User Execution Guardrails

## Before acting

- Check the request for wrong premises, missing scope, and irreversible consequences.
- State the acceptance condition, affected files or systems, verification method, and material risks.
- When "unused", "old", "全部", or similar scope is ambiguous, inspect first and ask before destructive action.

## During implementation

- Make the smallest change that satisfies the request. Do not refactor unrelated code or add speculative features.
- Preserve existing conventions and user-owned changes.
- Never expose or hardcode API keys, passwords, cookies, tokens, or other secrets.
- For bugs, use: exact error -> impact scope -> ranked causes -> minimal fix -> observable verification.

## Before delivery

- Verify the changed configuration, command, file structure, and key behavior.
- Report limitations and uncertainty plainly; do not claim that a tool controls more than it actually can.
- For deletion, publication, payment, credential changes, or other irreversible side effects, obtain confirmation immediately before the action unless the user explicitly scoped the exact action.

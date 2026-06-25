---
name: debugging-methodology
description: Use when encountering any bug, error, crash, test failure, or unexpected behavior — before proposing or making any code change. Enforces 5-step diagnostic discipline: restate error, scope impact, enumerate causes, choose minimal fix, define verification.
---

# Debugging Methodology

## Overview

Before ANY code change, run 5 diagnostic steps. Never skip. Never "just try something."

This is a **RIGID** discipline skill. Violate the steps = violate the skill.

**Foundational principle:** Guessing wastes time. Diagnosing saves it. Every fix without diagnosis is a gamble.

## When to Use

- Any error message, traceback, or crash
- Test failure (unit, integration, e2e)
- Unexpected behavior ("it does X but should do Y")
- Regression ("it used to work")
- User reports bug

**Do NOT trigger** for: feature requests, design discussions, prose/formatting changes, questions without errors.

## The 5 Steps

### Step 1: Restate the Error

Quote the **exact** error message. Full traceback if available. No paraphrasing, no summarizing.

```
# Good
TypeError: mkstemp() got an unexpected keyword argument 'encoding'

# Bad
"there was some kind of file error"
```

### Step 2: Determine Impact Scope

List **every** file and function the error touches. Be explicit.

```
"This breaks:
- claude_client.py:chat_with_claude_cli() — cannot write prompt to temp file
- bridge.py:main() — fails on import  
- webhook_server.py — never reached, Flask can't start"
```

### Step 3: List Possible Causes

At least 2-3 root causes, ranked by likelihood. Don't just pick the first one.

```
1. (most likely) Python 3.11 mkstemp() doesn't accept 'encoding' — added in 3.12
2. (less likely) tempfile module corrupted or shadowed
3. (unlikely) filesystem permission issue on temp directory
```

### Step 4: Choose Minimal Fix

Pick the fix that changes the **fewest lines**, removes the **least code**, has the **lowest side-effect risk**. State WHY.

```
Minimal fix: Remove 'encoding' parameter from mkstemp() call (1 line).
The fdopen() call already sets encoding on the file handle.
This is Python 3.11 compatible and doesn't change behavior.
```

### Step 5: Explain Verification

One command or action that proves the fix worked. Must be **observable** (exit code, output, status change).

```
python -c "from claude_client import chat_with_claude_cli; print('OK')"
→ exits 0, prints "OK"
```

## After the Fix

Report 3 things:
1. **What was wrong** (the root cause)
2. **What you changed** (the diff)
3. **Whether verification passed** (the output)

## Red Flags — STOP and Go Back to Step 1

| Thought | Action |
|---------|--------|
| "Maybe I should just try..." | STOP. Go to step 1. |
| "This is probably just a..." | STOP. Go to step 3. List all causes. |
| "Let me change a few things and see..." | STOP. Go to step 4. Pick ONE minimal fix. |
| "I'll fix it and check if it works" | STOP. Go to step 5. Define verification FIRST. |

## No Exceptions

- Not for "obvious one-liners" — even typos need step 1-2-5
- Not for "I already know the fix" — still run steps 3-4 before touching code
- Not for "the error is clear" — clarity is an assumption until verified
- Not for urgency — rushing causes more bugs

## Real-World Example

From session 2026-06-25, feishu-claude-bridge debugging:

**Step 1: Error**
```
SyntaxError: invalid character '。' (U+3002) at feishu_client.py:58
```

**Step 2: Scope**
- `feishu_client.py` — entire file unimportable, 8 corrupted docstrings
- `webhook_server.py` — partially corrupted (fixed earlier)  
- `config.py` — partially corrupted (fixed earlier)
- Root cause: PowerShell `Set-Content` default encoding (Windows-1252) truncated UTF-8 multibyte Chinese characters

**Step 3: Causes**
1. (confirmed) PowerShell `Set-Content` without `-Encoding UTF8` corrupted files
2. (ruled out) Python source file encoding declaration missing
3. (ruled out) git checkout corruption

**Step 4: Minimal fix**
Rewrite affected files with English docstrings using the Write tool (UTF-8 safe). Avoid regex-based edits on UTF-8 files from PowerShell.

**Step 5: Verification**
```
python bridge.py
→ [OK] 配置校验通过, Server: 0.0.0.0:8080, no SyntaxError
```

---
name: skills-governance
description: After task completion or session end, analyze learnings and recommend: should this become a skill, a workflow, or neither? Audit installed skills for overlap, staleness, and scenario-fit drift. Keep the skill ecosystem lean and correctly triggered.
---

# Skills Governance & Refinement

After significant tasks or at session end, audit what was learned and how the skill ecosystem should evolve.

## Part 1: Learning Capture

For each non-obvious thing learned during the session, classify it:

### Skill-worthy (create or update a skill)
A learning should become a skill when:
- The same approach will be reused across sessions with different inputs
- The knowledge is procedural (steps, checks, decision trees) not just factual
- Getting it wrong has meaningful consequences
- The pattern applies to a recognizable trigger phrase or context

### Workflow-worthy (create an automated workflow)
A learning should become a workflow when:
- The task is multi-step with branching logic
- Steps can run in parallel or have dependencies
- It benefits from adversarial verification (multiple agents checking each other)
- It's large enough to need phase grouping

### Memory-worthy (save to memory)
A learning should become a memory when:
- It's a fact, preference, or past decision, not a procedure
- It's context that future sessions should know but doesn't need active instructions

### Neither (discard)
Don't capture:
- Things already covered by existing skills or CLAUDE.md
- One-off trivia that won't apply to future sessions
- Information derivable from the codebase itself

## Part 2: Skill Layering & Conflict Detection

After every skill install or update, run these checks:

### Layer Check
Skills form layers. Higher layers override lower:
1. **User skills** (personal, cross-project) — `~/.claude/skills/`
2. **Project skills** (repo-specific) — `.claude/skills/`
3. **Plugin skills** (from marketplaces) — managed by plugin system

When two skills address the same scenario:
- More specific wins over more general
- Project-local wins over global
- Confirm that the less-specific skill still triggers correctly for its other scenarios

### Overlap Detection
For the newly installed/updated skill, check against existing skills:
- Does any existing skill have overlapping trigger phrases?
- If yes: which one should win for each shared scenario?
- Document the boundary in the more general skill's description

### Staleness Check
For each installed skill, periodically ask:
- When was this last used successfully?
- Has the underlying tool/API it depends on changed?
- Do the trigger phrases still match what users actually say?

## Part 3: Correctness Over Time

Skills must stay correct in their triggering scenarios. After each session where a skill was used:

1. Did the skill trigger at the right time?
2. Did it fail to trigger when it should have?
3. Did it trigger when it shouldn't have?
4. Were its instructions still accurate and complete?

If any answer is "no," flag the skill for refinement.

## Output Format

After session-end or on request, produce:

```
## Skills Governance Report

### Learnings Captured
- [learning] → [skill/workflow/memory/none] → [reason in one sentence]

### Overlap Detected
- [skill A] overlaps with [skill B] on [shared scenario] → [resolution]

### Skills Needing Refinement
- [skill name]: [what's wrong] → [suggested fix]
```

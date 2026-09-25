---
name: refine-skill-governance
description: Evaluate completed-task learnings and recommend whether to retain them as a reusable skill, an automated workflow, both, or neither. Use at substantive task closeout or when refining, layering, deduplicating, validating, or governing installed skills so each skill continues to trigger only in the correct scenario.
---

# Refine Skill Governance

Turn task results into a small, durable retention recommendation without automatically creating or rewriting skills or automations.

## Decide What to Retain

1. Extract only demonstrated, reusable learning from the conversation and result. Exclude secrets, transient errors, guesses, and details already covered by an installed skill.
2. Choose one outcome:
   - `Neither`: one-off work, weak evidence, or no reusable improvement.
   - `Skill`: contextual judgment, domain rules, tool-selection logic, or a reusable procedure that should trigger from future requests.
   - `Automation`: deterministic recurring execution driven by time, an event, or an external-state check.
   - `Both`: an automation supplies scheduling and state, while a skill supplies non-deterministic reasoning or a specialized procedure. Keep the source of truth in one place and reference it from the other.
3. Recommend creation or modification only when the expected reuse value exceeds the added trigger and maintenance complexity.

Do not create an automation, edit installed skills, or send external actions unless the user explicitly authorizes that change.

## Govern the Skill Portfolio

Assign each proposed or installed skill to one layer:

- `L0 System`: platform-owned primitives; do not modify locally.
- `L1 Guardrail`: cross-task safety and quality checks.
- `L2 Domain`: reusable reasoning for a business or knowledge domain.
- `L3 Tool/Workflow`: procedures tied to a tool, format, repository, or integration.
- `L4 Experimental`: unproven, overlapping, or environment-specific skills pending validation.

Apply these governance rules:

1. Give each behavior one primary owner. Prefer refining the owner over creating an overlapping skill.
2. Put positive trigger conditions and important exclusions in the frontmatter description.
3. Prefer the narrowest applicable domain or tool skill; allow guardrail skills to compose with it.
4. Record dependencies, compatibility assumptions, validation examples, counterexamples, and a last-verified condition when they matter.
5. Move a skill through `proposed -> experimental -> stable -> deprecated -> archived`; promote only after successful real use and counterexample testing.
6. When overlap exists, recommend merge, boundary tightening, precedence, or deprecation. Never silently mass-edit the portfolio.

## Recommendation Format

Return a compact recommendation containing:

- Learning observed
- Retention choice: `Neither`, `Skill`, `Automation`, or `Both`
- Proposed trigger and explicit non-trigger boundary
- Governance layer and relationship to installed skills
- Minimum validation needed before promotion

If nothing material should be retained, say `本轮无值得新增或改写的 Skill/自动化` and explain why in one sentence.

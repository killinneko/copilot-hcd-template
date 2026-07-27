---
name: refactor-code
description: Refactor code while preserving behavior and proving equivalence with tests.
agent: Implementation
argument-hint: "target, reason, constraints, and behavior that must remain unchanged"
---

Inspect the target and identify the concrete maintainability problem. Define invariants and tests that protect behavior, then make the smallest useful refactor. Avoid mixing unrelated feature changes. Run relevant checks and report structural improvements, unchanged behavior, and residual risks.


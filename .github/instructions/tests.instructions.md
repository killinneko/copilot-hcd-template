---
applyTo: "**/{test,tests,__tests__}/**/*,**/*.{test,spec}.{py,ts,tsx,js,jsx}"
---

# Test instructions

- Test externally observable behavior rather than implementation details.
- Include normal, boundary, invalid-input, and failure cases where relevant.
- Keep tests deterministic and independent.
- Name tests so the expected behavior and condition are clear.
- Mock only external boundaries; avoid mocking the unit under test.
- For accessibility-sensitive UI, include keyboard and accessible-name checks.


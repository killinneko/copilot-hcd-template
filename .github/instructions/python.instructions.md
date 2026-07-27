---
applyTo: "**/*.py"
---

# Python instructions

- Use type hints for public functions and non-obvious data structures.
- Prefer small, testable functions with explicit inputs and outputs.
- Raise specific exceptions with actionable messages.
- Do not use mutable default arguments.
- Keep I/O, transformation, and presentation logic separate.
- For pandas code, avoid silent chained assignment and document required columns.
- For Streamlit, cache only deterministic or resource-heavy work and choose `st.cache_data` or `st.cache_resource` deliberately.
- Run the project's formatter, linter, type checker, and tests when configured.


# Repository instructions

## Source of truth

- Before changing code, read `README.md` and `docs/templates/project-context.md`.
- Treat existing code, tests, configuration, and documented decisions as the source of truth.
- If required context is missing, state assumptions explicitly and choose the smallest reversible change.

## Working style

- Start by restating the intended outcome and acceptance criteria.
- Inspect relevant files before proposing or implementing changes.
- Keep changes focused; do not modify unrelated files.
- Preserve existing public APIs and user-visible behavior unless the task explicitly changes them.
- Prefer simple, maintainable solutions over premature abstraction.
- Never invent research findings, user quotes, metrics, test results, or accessibility compliance.

## HCD and UX

- Identify the target user, goal, context of use, and primary task before making significant UI decisions.
- Separate observed facts, evidence-based interpretations, assumptions, and design decisions.
- Use personas only when they are grounded in research data; label provisional personas clearly.
- Choose visualizations from the user question and data characteristics, not aesthetics alone.
- Provide loading, empty, error, and success states for interactive interfaces.
- Use WCAG 2.2 AA as the accessibility target unless the project specifies another standard.

## Engineering

- Follow the repository's existing language, framework, formatting, and testing conventions.
- Validate inputs at system boundaries and avoid exposing secrets or personal data.
- Add or update tests for changed behavior.
- Run the narrowest relevant checks first, then broader checks where practical.
- Report commands run, results, remaining risks, and anything not verified.

## Documentation

- Update documentation when setup, behavior, interfaces, or user workflows change.
- Keep the root `README.md` as the overview and navigation entry point.
- Put procedural guides in `docs/how-to/`, reference material in `docs/reference/`, and reusable forms in `docs/templates/`.


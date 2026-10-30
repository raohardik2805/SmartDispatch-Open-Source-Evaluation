# AI-Use Declaration

- Tool: OpenAI ChatGPT (GPT-6).
- Purpose: Repository inspection, implementation assistance, regression-test drafting, and documentation drafting.
- Verification: The branch's GitHub Actions workflow ran `python -m pytest -q` (247 passed) and `python -m main` successfully. The student should still review the implementation and understand the documented assumptions.
- Displayed credits/tokens: Not available.
- Suggestion accepted: Validate numeric time inputs as finite non-negative numbers and reject booleans, because Python treats booleans as integers.
- Suggestion changed/rejected: No performance optimization was claimed without a benchmark.
- Disclosure: The student reports that the instructor verbally authorized AI assistance. The repository's written policy also contains a prohibition on AI-generated code/tests; retain the instructor's clarification if requested during evaluation.

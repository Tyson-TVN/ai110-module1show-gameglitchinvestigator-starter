# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

**Prompt used (Challenge 1):**

```text
Challenge 1: Advanced Edge-Case Testing. Pick edge-case inputs that could still break the game (empty input, non-numeric text, negative numbers, decimals, extremely large values) and write pytest cases in tests/test_game_logic.py that check they are handled gracefully. parse_guess is still in app.py, so move it into logic_utils.py unchanged, import it in app.py, and test it there. Do not change how parse_guess behaves; the tests should describe what it does today. Keep each test short with a clear name.
```

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Empty input `""` | Challenge 1 prompt above | `test_empty_string_is_rejected`: `parse_guess("")` returns `(False, None, "Enter a guess.")` | Yes | Pressing Submit with an empty box is the most common accidental input, so it must show a message instead of crashing. |
| Non-numeric text (`"abc"`, `"12abc"`, `"   "`, `"1e3"`) | Challenge 1 prompt above | `test_non_numeric_text_is_rejected`: each returns `(False, None, "That is not a number.")` | Yes | Players type words, mixed text, blanks and scientific notation; `int()` raises `ValueError` for all of these, so I wanted to confirm they are caught. |
| Negative number (`"-5"`) | Challenge 1 prompt above | `test_negative_number_is_parsed_without_crashing`: returns `(True, -5, None)` | Yes | A negative value is outside every difficulty range. The test records that it does not crash; `parse_guess` does not check the range, so the hint logic handles it as "Too Low". |
| Decimal (`"7.9"`) | Challenge 1 prompt above | `test_decimal_guess_is_truncated_to_int`: returns `(True, 7, None)` | Yes | The code takes the `float()` path for any input with a dot, so I wanted to pin down that it truncates instead of rejecting. |
| Extremely large values (`"99999999999999999999"`, `"1.5e400"`) | Challenge 1 prompt above | `test_huge_values_do_not_crash`: the large integer parses, and `"1.5e400"` (which overflows `float` to infinity) returns "not a number" | Yes | A huge decimal makes `int(float(...))` raise `OverflowError`; the broad `except Exception` catches it, and the test makes sure that stays true. |

**Refactor needed for the tests:** `parse_guess` was still in `app.py`, so I moved it unchanged into `logic_utils.py` and imported it in `app.py` so the tests could import it.

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->

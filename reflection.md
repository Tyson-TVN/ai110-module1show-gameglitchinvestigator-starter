# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The Streamlit game loaded and looked normal, with a difficulty selector, a guess box, Submit and New Game buttons, and a debug panel. Once I started playing, the behavior was wrong. The New Game button did nothing, the difficulty ranges made no sense, the hints pointed the wrong way, and the secret number could fall outside the selected range.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  **Concrete bugs I noticed:** (line numbers refer to the original starter `app.py` before my changes)

1. **New Game button does nothing.**
   - Trigger: clicking "New Game" during a game or after a win/loss.
   - Expected: the game fully resets (new secret, attempts, score, history and status) and shows a confirmation.
   - Actual: nothing visibly changes. After a win or loss the game stays stuck on "Game over".
   - Cause: the handler in `app.py` (lines 134-138) only resets `attempts` and `secret`, then calls `st.rerun()` right after `st.success(...)`, so the message never displays. It never resets `status`, `score` or `history`, so the `st.stop()` guard (lines 140-145) keeps blocking play.

2. **Difficulty ranges are inconsistent.**
   - Trigger: switching between Easy, Normal and Hard and reading the sidebar range.
   - Expected: the range grows with difficulty, so Hard has the widest range.
   - Actual: Easy is 1-20, Normal is 1-100 and Hard is 1-50. Hard has a smaller range than Normal, which makes it easier to guess.
   - Cause: `get_range_for_difficulty` in `app.py` (lines 4-11) returns the wrong range for "Hard".

3. **Hints are backwards (for example, a guess of 1 says "Go lower").**
   - Trigger: entering 1, the lowest possible number, when the secret is higher.
   - Expected: "Too Low" with the hint "Go HIGHER!". It is impossible to go lower than 1.
   - Actual: the game shows "Go LOWER!".
   - Cause: in `check_guess` in `app.py` (lines 37-40, repeated in the fallback at lines 45-47), the hint messages are swapped. A guess greater than the secret returns "Go HIGHER!" and a guess lower than the secret returns "Go LOWER!".

4. **Secret number is outside the selected range.**
   - Trigger: starting on the default difficulty (Normal), switching to Easy (1-20), then checking the Debug Info.
   - Expected: on Easy the secret is always between 1 and 20.
   - Actual: the secret was 91.
   - Cause: in `app.py` (lines 92-93) the secret is generated only once, when `"secret"` is first missing from `st.session_state`, using whichever difficulty was selected at that moment. Changing the difficulty later never regenerates it. The New Game handler (line 136) also hardcodes `random.randint(1, 100)` instead of using the selected range.


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output | Suspected Code Location |
|------------|-------------------|-----------------|------------------------|-------------------------|
| Click "New Game" mid-game or after a win/loss | Game resets fully and shows "New game started." | Nothing visible happens. After a win/loss it still shows "Game over" | none | `app.py` lines 134-138 (`st.rerun()` wipes the message, `status`/`score`/`history` not reset) and the guard at lines 140-145 |
| Compare the sidebar ranges for Easy, Normal and Hard | Range grows with difficulty (Hard widest) | Easy 1-20, Normal 1-100, Hard 1-50 | none | `app.py`, `get_range_for_difficulty` (lines 4-11) |
| Guess `1` when the secret is higher | "Too Low" with "Go HIGHER!" | Hint says "Go LOWER!" | none | `app.py`, `check_guess` (lines 37-40, 45-47) |
| Start on Normal, switch to Easy, open Debug Info | Secret between 1 and 20 | Secret was 91 | none | `app.py` lines 92-93 (secret created once) and line 136 (New Game hardcodes 1-100) |

**Game Run Trace (before any fixes)**

```
Command: python -m streamlit run app.py   (Normal difficulty by default)

Run 1 - Hints
  Opened "Developer Debug Info" -> secret was higher than 1
  Entered guess 1 -> Submit
  Game showed: "Go LOWER!"   (expected "Go HIGHER!", 1 is the lowest possible number)

Run 2 - Secret out of range
  Started on Normal, switched Difficulty to Easy (sidebar: "Range: 1 to 20")
  Opened "Developer Debug Info" -> Secret: 91   (expected 1-20)

Run 3 - Reset
  Clicked "New Game" mid-game -> no visible message or change

Run 4 - Ranges
  Sidebar ranges: Easy 1 to 20, Normal 1 to 100, Hard 1 to 50  (Hard narrower than Normal)
```

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

**AI tools used:** I used Claude as the AI coding assistant in VS Code. I used a separate chat for each bug and for writing tests, and one more chat as a helper that planned the work and reviewed each diff before I committed.

**A correct suggestion:** For the backwards hints I asked the assistant to move `check_guess` into `logic_utils.py`, fix the hints and update the import in `app.py`. It swapped the hint messages so that "Too High" says "Go LOWER!" and "Too Low" says "Go HIGHER!", kept the `(outcome, message)` return shape and left every other function alone. It was correct because the hint now matches the real relationship between the guess and the secret. I verified it by reading the diff, running pytest (tests for 60 vs 50, 40 vs 50 and 1 vs 50), and playing the game, where a guess of 1 now says "Go HIGHER!". The same chat also caught that the three starter tests compared the returned tuple to a plain string and would fail, which was a real catch.

**A suggestion I did not accept as written:** The helper chat first told me that the string conversion of the secret on even attempts meant I could never win on even attempts. That was wrong. When I read `check_guess` the `TypeError` fallback compares `str(guess)` to the string secret, so an exact guess still wins. Only the hints are wrong on those attempts, because `"100" < "97"` as text. I checked this in the live game: with secret 97, guess 100 said "Go HIGHER!" (wrong hint) while guess 97 still won. I corrected the explanation and fixed the real problem by passing the integer secret to `check_guess` instead of the string.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

**How I decided a bug was fixed:** Where a bug could be tested I wrote a pytest case for it, confirmed the fix made it pass, and then repeated the exact steps that triggered the bug in the running game. A fix only counted when the game behaved correctly.

**Tests I ran:** In `tests/test_game_logic.py` I tested hints (60 vs 50 gives "Too High" with "LOWER", 40 vs 50 and 1 vs 50 give "Too Low" with "HIGHER", and 100 vs 97 is "Too High"), plus the ranges from `get_range_for_difficulty` (Easy is 1-20, Normal is 1-100, unknown difficulty defaults to 1-100, and low < high for every level). All tests pass with plain `pytest`. The three starter tests also exposed a problem: they compared the whole `(outcome, message)` tuple to a string and failed until I unpacked the tuple. The `check_guess(100, 97)` test passes with or without the fix in `app.py`, because that bug was in how `app.py` called `check_guess`, so I checked that fix by playing several guesses in a row and comparing each hint with the secret in Debug Info.

**What manual checks showed:** With the secret visible in Debug Info, a guess of 1 shows "Go HIGHER!", and switching from Normal to Easy and clicking New Game always gives a secret between 1 and 20. Before the last fix, secret 97 with guess 100 gave "Go HIGHER!", which led me to the string-compare bug on even attempts.

**Setup problem:** Plain `pytest` failed with `ModuleNotFoundError: No module named 'logic_utils'`, while `python -m pytest` worked. I fixed it by adding a `pytest.ini` with `pythonpath = .`.

**How AI helped with tests:** I gave the assistant the exact cases to cover and told it not to assert Hard's range, because that range is still one of the documented bugs and I didn't want a test to lock it in. It also flagged that one of my requested tests duplicated an existing one, so I removed it.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit reruns the whole script from top to bottom every time you click a button or change a widget, so normal variables are reset each time. `st.session_state` is a dictionary that survives those reruns, which is where the game keeps the secret number, attempts and score. The secret bug came from this: the secret was stored once at startup and never updated when the difficulty changed, so I added a `secret_difficulty` key to detect the change.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

**Habit to reuse:** I want to keep working on one bug per chat, marking the problem with a `# FIXME` comment first, and committing after every fix. It kept the AI's changes small enough to review line by line.

**What I would do differently:** I would run the tests and the game myself before trusting any summary. Chat A said it hadn't run anything, and the helper chat made a wrong claim about even attempts that I only caught by reading the code.

**How this changed my view of AI code:** AI-written code can look clean and still be wrong, and its explanations can be wrong too, so I now treat each suggestion as a hypothesis to test rather than an answer.

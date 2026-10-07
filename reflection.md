# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The Streamlit game loaded and looked normal, with a difficulty selector, a guess box, Submit and New Game buttons, and a debug panel. Once I started playing, the behavior was wrong. The New Game button did nothing, the difficulty ranges made no sense, the hints pointed the wrong way, and the secret number could fall outside the selected range.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  **Concrete bugs I noticed:**

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


---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

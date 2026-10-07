# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Purpose:** A Streamlit number-guessing game. The player picks a difficulty, guesses the secret number, and gets Higher/Lower hints within a limited number of attempts. This project started from an AI-generated version full of bugs, and the goal was to find, explain, fix and test them.

**Bugs found:** (details with reproduction steps are in `reflection.md`)
- Hints were backwards ("Go LOWER!" for a guess below the secret).
- The secret could fall outside the selected range (for example 91 on Easy, 1-20).
- The New Game button appeared to do nothing and did not reset the game.
- Difficulty ranges were inconsistent (Hard 1-50 is narrower than Normal 1-100).
- On even attempts the secret was converted to a string, so the hints used text comparison.

**Fixes applied:**
- Moved `check_guess` and `get_range_for_difficulty` into `logic_utils.py` and imported them in `app.py`.
- Swapped the hint messages in `check_guess` so the hints match the guess.
- Regenerated the secret when the difficulty changes, and made New Game use the selected difficulty's range (`secret_difficulty` in `st.session_state`).
- Passed the integer secret to `check_guess` on every attempt.
- Added pytest tests and a `pytest.ini` so plain `pytest` works.

**Not fixed:** the New Game button still does not reset the status, score and history, and the Hard range (1-50) is still narrower than Normal. Both are documented in `reflection.md`. I also noticed that the attempts counter starts at 1 and the "Guess a number between 1 and 100" banner ignores the difficulty, and left both alone.


## 📸 Demo Walkthrough

1. Choose **Easy** in the sidebar. It shows "Range: 1 to 20" and the secret is between 1 and 20.
2. Open "Developer Debug Info" and see the secret, for example 12.
3. Enter 1 and click Submit. The game says "Go HIGHER!".
4. Enter 20 and click Submit. The game says "Go LOWER!".
5. Enter 12 and click Submit. The game shows balloons and "You won! The secret was 12."
6. Switch to **Normal** and the secret is regenerated within 1-100.


**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
rootdir: C:\Users\thota\ai110-module1show-gameglitchinvestigator-starter
configfile: pytest.ini
plugins: anyio-4.15.1
collected 11 items                                                                            

tests\test_game_logic.py ...........                                                    [100%]

===================================== 11 passed in 0.11s =====================================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]

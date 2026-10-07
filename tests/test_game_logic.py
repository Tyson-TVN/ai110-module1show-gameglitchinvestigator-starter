from logic_utils import check_guess, get_range_for_difficulty, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_too_high_tells_player_to_go_lower():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_too_low_tells_player_to_go_higher():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_lowest_guess_tells_player_to_go_higher():
    outcome, message = check_guess(1, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_three_digit_guess_vs_two_digit_secret_is_numeric():
    outcome, message = check_guess(100, 97)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_easy_range_is_1_to_20():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_normal_range_is_1_to_100():
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_unknown_difficulty_defaults_to_1_to_100():
    assert get_range_for_difficulty("Impossible") == (1, 100)

def test_low_is_less_than_high_for_every_difficulty():
    for difficulty in ["Easy", "Normal", "Hard"]:
        low, high = get_range_for_difficulty(difficulty)
        assert low < high

# Edge cases for parse_guess

def test_empty_string_is_rejected():
    ok, guess, error = parse_guess("")
    assert ok is False
    assert guess is None
    assert error == "Enter a guess."

def test_non_numeric_text_is_rejected():
    for raw in ["abc", "12abc", "   ", "1e3"]:
        ok, guess, error = parse_guess(raw)
        assert ok is False
        assert guess is None
        assert error == "That is not a number."

def test_negative_number_is_parsed_without_crashing():
    # parse_guess only converts text to an int; it does not check the range
    assert parse_guess("-5") == (True, -5, None)

def test_decimal_guess_is_truncated_to_int():
    assert parse_guess("7.9") == (True, 7, None)

def test_huge_values_do_not_crash():
    ok, guess, _ = parse_guess("99999999999999999999")
    assert ok is True
    assert guess == 99999999999999999999
    ok, guess, error = parse_guess("1.5e400")
    assert ok is False
    assert error == "That is not a number."

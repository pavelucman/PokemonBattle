from app.battle_logic import calculate_total

def test_calculate_total_basic():
    stats = {"hp": 45, "attack": 50, "defense": 50, "speed": 40}
    assert calculate_total(stats) == 185

def test_calculate_total_empty():
    stats = {}
    assert calculate_total(stats) == 0

def test_calculate_total_missing_keys():
    stats = {"hp": 30, "attack": 20}
    assert calculate_total(stats) == 50
from sqlalchemy.orm import Session
from app.models import Battle
from app.services import get_or_create_pokemon

def calculate_total(stats: dict) -> int:
    return sum(stats.values())

def simulate_battle(db: Session, name1: str, name2: str) -> Battle:
    p1 = get_or_create_pokemon(db, name1)
    p2 = get_or_create_pokemon(db, name2)

    total1 = calculate_total(p1.base_stats)
    total2 = calculate_total(p2.base_stats)

    winner = p1 if total1 >= total2 else p2

    battle = Battle(pokemon_1_id=p1.id, pokemon_2_id=p2.id, winner_id=winner.id)
    db.add(battle)
    db.commit()
    db.refresh(battle)
    return battle
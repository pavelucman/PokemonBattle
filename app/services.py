import requests
from sqlalchemy.orm import Session
from app.models import Pokemon

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon/"

def get_or_create_pokemon(db: Session, name: str) -> Pokemon:
    name = name.lower()
    existing = db.query(Pokemon).filter_by(name=name).first()
    if existing:
        return existing

    res = requests.get(POKEAPI_URL + name)
    if res.status_code != 200:
        raise ValueError(f"Pokemon '{name}' not found")

    data = res.json()
    stats = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}

    pokemon = Pokemon(name=name, base_stats=stats)
    db.add(pokemon)
    db.commit()
    db.refresh(pokemon)
    return pokemon
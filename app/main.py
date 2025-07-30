from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Pokemon, Battle
from app.preload_pokemon import preload_pokemons

pokemon_list = ["pikachu", "bulbasaur", "charmander", "squirtle"]

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    preload_pokemons(pokemon_list)
    yield

app = FastAPI(lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/battle")
def simulate_battle(pokemon_1: str, pokemon_2: str, db: Session = Depends(get_db)):
    p1 = db.query(Pokemon).filter(Pokemon.name == pokemon_1.lower()).first()
    p2 = db.query(Pokemon).filter(Pokemon.name == pokemon_2.lower()).first()

    if not p1 or not p2:
        raise HTTPException(status_code=404, detail="One or both Pokémon not found.")

    score_1 = sum(p1.base_stats.values())
    score_2 = sum(p2.base_stats.values())
    winner = p1 if score_1 >= score_2 else p2

    battle = Battle(
        pokemon_1_id=p1.id,
        pokemon_2_id=p2.id,
        winner_id=winner.id
    )
    db.add(battle)
    db.commit()
    db.refresh(battle)

    return {
        "pokemon_1": p1.name,
        "pokemon_2": p2.name,
        "winner": winner.name
    }
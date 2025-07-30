from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import BattleCreate, BattleOut
from app.battle_logic import simulate_battle
from app.database import SessionLocal
from app.models import Battle, Pokemon
from app.schemas import PokemonOut

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/battle", response_model=BattleOut)
def battle(data: BattleCreate, db: Session = Depends(get_db)):
    try:
        result = simulate_battle(db, data.pokemon_1, data.pokemon_2)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"id": result.id, "winner": result.winner}


@router.get("/battles")
def list_battles(db: Session = Depends(get_db)):
    return db.query(Battle).all()

from pydantic import BaseModel
from typing import Dict

class PokemonBase(BaseModel):
    name: str

class PokemonCreate(PokemonBase):
    base_stats: Dict[str, int]

class PokemonOut(PokemonBase):
    id: int
    base_stats: Dict[str, int]

    class Config:
        orm_mode = True

class BattleCreate(BaseModel):
    pokemon_1: str
    pokemon_2: str

class BattleOut(BaseModel):
    id: int
    winner: PokemonOut
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Pokemon(Base):
    __tablename__ = "pokemon"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    hp = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)

    base_stats = Column(JSON, nullable=False)

    battles_as_pokemon_1 = relationship("Battle", foreign_keys='Battle.pokemon_1_id', back_populates="pokemon_1")
    battles_as_pokemon_2 = relationship("Battle", foreign_keys='Battle.pokemon_2_id', back_populates="pokemon_2")
    battles_won = relationship("Battle", foreign_keys='Battle.winner_id', back_populates="winner")


class Battle(Base):
    __tablename__ = "battle"

    id = Column(Integer, primary_key=True, index=True)
    pokemon_1_id = Column(Integer, ForeignKey("pokemon.id"), nullable=False)
    pokemon_2_id = Column(Integer, ForeignKey("pokemon.id"), nullable=False)
    winner_id = Column(Integer, ForeignKey("pokemon.id"), nullable=False)

    pokemon_1 = relationship("Pokemon", foreign_keys=[pokemon_1_id], back_populates="battles_as_pokemon_1")
    pokemon_2 = relationship("Pokemon", foreign_keys=[pokemon_2_id], back_populates="battles_as_pokemon_2")
    winner = relationship("Pokemon", foreign_keys=[winner_id], back_populates="battles_won")

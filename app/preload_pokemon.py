import requests
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:postgres@db:5432/pokemon"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Pokemon(Base):
    __tablename__ = 'pokemon'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    base_stats = Column(JSON, nullable=False)


def fetch_pokemon_data(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"Failed to fetch {name}")
        return None
    data = resp.json()
    stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
    return {
        'name': data['name'],
        'hp': stats.get('hp', 0),
        'attack': stats.get('attack', 0),
        'defense': stats.get('defense', 0),
        'base_stats': stats
    }


def preload_pokemons(pokemon_names):
    for name in pokemon_names:
        existing = session.query(Pokemon).filter_by(name=name).first()
        if existing:
            print(f"{name} already loaded.")
            continue

        data = fetch_pokemon_data(name)
        if data is None:
            continue

        pokemon = Pokemon(
            name=data['name'],
            hp=data['hp'],
            attack=data['attack'],
            defense=data['defense'],
            base_stats=data['base_stats']
        )
        session.add(pokemon)
        print(f"Added {name}")

    session.commit()
    print("Preloading complete.")


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    preload_list = ["pikachu", "bulbasaur", "charmander", "squirtle"]

    preload_pokemons(preload_list)
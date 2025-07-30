# Pokemon Battle

Pokemon Battle Simulator (Backend)
A REST API that simulates a battle between two Pokemons using data from PokeAPI. 
Results are stored in PostgreSQL and containerized with Docker.

## Installation
git clone https://github.com/pavelucman/PokemonBattle.git
cd PokemonBattle

## Run the application with Docker Compose
docker compose up --build

## API should now be available at
http://localhost:8000/docs

## Battle Algorithm
The battle algorithm fetches both Pokemons from PokeAPI and calculates the sum of their base stats (HP, Attack, Defense, etc.).
If equal, the first wins.

Example:
Pikachu: [35 HP, 55 Attack, 40 Defense, 90 Speed] → Total: 220
Charmander: [39 HP, 52 Attack, 43 Defense, 65 Speed] → Total: 199
Winner: Pikachu

## API Endpoints
- `POST /battle` — Starts a new battle between two Pokemons
- `GET /battles` — Retrieves the list of past battles

Example request:
{
  "pokemon_1": "pikachu",
  "pokemon_2": "charmander"
}

Response:
{
  "pokemon_1": "pikachu",
  "pokemon_2": "charmander",
  "winner": "pikachu"
}

GET /battles
Returns all past battles.

## Unit Testing
docker compose exec web pytest

Tests are located in the tests/ directory.

## Technologies
- Python 3.10
- FastAPI
- PostgreSQL
- Docker Compose
- PokeAPI
- SQLAlchemy
- Pytest
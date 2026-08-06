import os

from dotenv import load_dotenv


load_dotenv()


BASE_URL = os.getenv(
    "BASE_URL",
    "https://api.pokemonbattle.ru/v2",
)

TRAINER_ID = int(
    os.getenv("TRAINER_ID", "64605")
)

TOKEN = os.getenv("TOKEN", "")

LAVKA_URL = os.getenv(
    "LAVKA_URL",
    "https://lavka.pokemonbattle.ru",
)
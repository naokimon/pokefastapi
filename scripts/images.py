import pandas as pd

AMOUNT_OF_POKEMONS = 1025

df = pd.read_csv("../data/pokemon.csv")

base_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/"

df["image_uri"] = base_url + df["ID"].astype(str) + ".png"

df.to_csv("../data/pokemon.csv", index=False)
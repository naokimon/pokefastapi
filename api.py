from fastapi import FastAPI, HTTPException
from db import search_pokemon

app = FastAPI()

@app.get("/")
def read_root():
    return {"Root": "This is the root of the API."}

@app.get("/pokemon/{identifier}")
async def get_pokemon(identifier: str):
    data = await search_pokemon(identifier)
    if data:
        pokemon = {
            "id": data["id"],
            "name": data["name"],
            "form": data["form"] if len(data["form"]) > 1 else None,
            "gen": data["generation"],
            "types": [
                {
                    "slot": 1,
                    "type": {
                        "name": data["type1"]
                    }
                }
            ],
            "stats": [],
        }

        if data["type2"]:
            type2 = {
                "slot": 2,
                "type": {
                    "name": data["type2"]
                }
            }

            pokemon["types"].append(type2)

        stats = ["hp","attack","defense","special_attack","special_defense","speed"]

        for stat in stats:
            stat_data = {
                "base_stat": data[stat],
                "stat": {
                    "name": stat
                }
            }

            pokemon["stats"].append(stat_data)

        return pokemon
    else:
        raise HTTPException(status_code=404, detail="Pokemon not found!")
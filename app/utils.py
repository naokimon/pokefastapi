def parsepokemon(data: dict):
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

    if len(data["type2"]) > 1:
        type2 = {
            "slot": 2,
            "type": {
                "name": data["type2"]
            }
        }

        pokemon["types"].append(type2)

    stats = ["hp", "attack", "defense", "special_attack", "special_defense", "speed"]

    for stat in stats:
        stat_data = {
            "base_stat": data[stat],
            "stat": {
                "name": stat
            }
        }

        pokemon["stats"].append(stat_data)

    return pokemon
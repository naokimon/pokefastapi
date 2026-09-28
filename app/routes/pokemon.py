from fastapi import APIRouter, HTTPException, Request
import app.db as db
from app.utils import parsepokemon

router = APIRouter()

@router.get("/pokemon")
async def get_pokemons(request: Request, limit: int = 20, offset: int = 0, sort: str = "", direction: str = "ASC"):
    if limit > 0 or offset > 0:
        if len(sort) > 1:
            allowed_sorts: list[str] = ["id", "name", "form", "type1", "type2", "total", "hp", "attack", "defense", "special_attack", "special_defense", "speed", "generation"]
            allowed_direction: list[str] = ["ASC", "DESC"]
            sort = sort.lower()
            direction = direction.upper()
            if sort in allowed_sorts and direction in allowed_direction:
                data: dict = await db.get_pokemons(limit, offset, sort=sort, direction=direction)
            else:
                raise HTTPException(status_code=400, detail=f"The sort: {sort} or (and) direction: {direction} is invalid!")
        return_data = {
            "count": len(data),
            "next": str(
                request.url.include_query_params(
                    limit=limit,
                    offset=offset + limit,
                    sort=sort if len(sort) > 1 else None,
                    direction=direction if len(sort) > 1 else None
                )
            ),
            "previous": str(
                request.url.include_query_params(
                    limit=limit,
                    offset=offset - limit,
                    sort=sort if len(sort) > 1 else None,
                    direction=direction if len(sort) > 1 else None
                )
            ) if offset > 0 else None,
            "results": []
        }
        for pokemon_data in data:
            pokemon = parsepokemon(pokemon_data)
            return_data["results"].append(pokemon)
        return return_data
    else:
        raise HTTPException(status_code=404, detail="Limit and or Offset must be greater then 0!")

@router.get("/pokemon/{identifier}")
async def get_pokemon(identifier: str):
    data = await db.search_pokemon(identifier)
    if data:
        return parsepokemon(data)
    else:
        raise HTTPException(status_code=404, detail="Pokemon not found!")

# @router.get("/debug")
# async def debug(request: Request):
#     return {
#         "url": str(request.url),
#         "host": request.headers.get("host"),
#         "server": request.scope.get("server"),
#         "scheme": request.url.scheme,
#     }
from fastapi import APIRouter, HTTPException, Request
import app.db as db
from app.utils import parsepokemon

router = APIRouter()

@router.get("/pokemon")
async def get_pokemons(request: Request, limit: int = 20, offset: int = 0):
    if limit > 0:
        data: dict = await db.get_pokemons(limit, offset)
        return_data = {
            "count": len(data),
            "next": str(request.url.include_query_params(limit=limit, offset=offset + limit)),
            "previous": str(request.url.include_query_params(limit=limit, offset=offset - limit)) if offset > 0 else None,
            "results": []
        }
        for pokemon_data in data:
            pokemon = parsepokemon(pokemon_data)
            return_data["results"].append(pokemon)
        return return_data
    else:
        raise HTTPException(status_code=404, detail="Limit must be greater then 0!")

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
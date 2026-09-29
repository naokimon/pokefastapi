from fastapi import APIRouter, HTTPException, Request, Depends
import app.db as db
from app.ratelimit import limiter
from app.db import count_pokemons
from app.utils import parsepokemon
from app.schemas import PokemonsResponse, PokemonResponse

router = APIRouter()

@router.get("/pokemon", response_model=PokemonsResponse)
@limiter.limit("2/1second")
async def get_pokemons(request: Request, limit: int = 20, offset: int = 0, sort: str = "", direction: str = "ASC"):
    if limit > 0 or offset >= 0:
        if len(sort) > 1:
            allowed_sorts: list[str] = ["id", "name", "form", "type1", "type2", "total", "hp", "attack", "defense", "special_attack", "special_defense", "speed", "generation"]
            allowed_direction: list[str] = ["ASC", "DESC"]
            sort = sort.lower()
            direction = direction.upper()
            if not sort in allowed_sorts and not direction in allowed_direction:
                raise HTTPException(status_code=400, detail=f"The sort: {sort} or (and) direction: {direction} is invalid!")

        data: dict = await db.get_pokemons(limit, offset, sort=sort, direction=direction)

        params = {
            "limit": limit,
            "sort": sort,
            "direction": direction
        }

        if not sort:
            params.pop("sort")
            params.pop("direction")

        db_length = await count_pokemons()

        offset = min(db_length, offset)

        return_data = {
            "count": len(data),
            "next": str(
                request.url.include_query_params(
                    **params,
                    offset=offset + limit
                )
            ) if offset < (db_length - 1) else None,
            "previous": str(
                request.url.include_query_params(
                    **params,
                    offset=max(0, offset - limit)
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

@router.get("/pokemon/{identifier}", response_model=PokemonResponse)
@limiter.limit("2/1second")
async def get_pokemon(request: Request, identifier: str):
    data = await db.search_pokemon(identifier.capitalize())
    if data:
        return parsepokemon(data)
    else:
        raise HTTPException(status_code=404, detail="Pokemon not found!")

@router.get("/debug")
@limiter.limit("2/1second")
async def debug_ip(request: Request):
    return {
        "client": request.client.host if request.client else None,
        "forwarded_for": request.headers.get("x-forwarded-for"),
        "real_ip": request.headers.get("x-real-ip"),
    }
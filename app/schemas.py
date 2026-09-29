from pydantic import BaseModel

class PokemonTypeBase(BaseModel):
    slot: int
    type: dict[
        str, str
    ]

class PokemonStatsBase(BaseModel):
    base_stat: int
    stat: dict[
        str, str
    ]

class PokemonResponse(BaseModel):
    id: int
    name: str
    form: str | None
    gen: int
    image_uri: str
    types: list[PokemonTypeBase]
    stats: list[PokemonStatsBase]

class PokemonsResponse(BaseModel):
    count: int
    next: str | None
    previous: str | None
    results: list[PokemonResponse]

class DebugResponse(BaseModel):
    client: str | None
    forwarded_for: str | None
    real_ip: str | None
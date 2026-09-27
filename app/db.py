import aiosqlite

DATABASE = "app/app.db"

async def get_pokemons(limit: int, offset: int = 0):
    async with aiosqlite.connect(DATABASE) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM pokemons LIMIT ? OFFSET ?",
            (limit, offset)
        )

        rows = await cursor.fetchall()

        return [dict(row) for row in rows]

async def search_pokemon(identifier: str):
    async with aiosqlite.connect(DATABASE) as db:
        db.row_factory = aiosqlite.Row
        if identifier.isnumeric():
            cursor = await db.execute(
                "SELECT * FROM pokemons WHERE id = ?",
                (identifier,)
            )
        else:
            cursor = await db.execute(
                "SELECT * FROM pokemons WHERE name = ?",
                (identifier,)
            )

        row = await cursor.fetchone()

        if row:
            return row
        else:
            return None
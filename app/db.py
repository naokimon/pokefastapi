import aiosqlite

DATABASE = "app.db"

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
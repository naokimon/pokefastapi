import aiosqlite
import os

DATABASE = os.getenv(DATABASE_PATH, "app/app.db")

async def count_pokemons():
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM pokemons"
        )

        rows = await cursor.fetchone()

        return rows[0]

async def get_pokemons(limit: int = 20, offset: int = 0, sort: str = "", direction: str = "ASC"):
    async with aiosqlite.connect(DATABASE) as db:
        db.row_factory = aiosqlite.Row
        if len(sort) > 1:
            cursor = await db.execute(
                f"SELECT * FROM pokemons ORDER BY {sort} {direction} LIMIT ? OFFSET ?",
                (limit, offset,)
            )
        else:
            cursor = await db.execute(
                "SELECT * FROM pokemons LIMIT ? OFFSET ?",
                (limit, offset,)
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
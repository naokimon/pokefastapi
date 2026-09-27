import csv
import aiosqlite

BATCH_SIZE = 200
DATABASE = "app.db"

async def init_db():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS pokemons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            form TEXT,
            type1 TEXT,
            type2 TEXT,
            total INTEGER,
            hp INTEGER,
            attack INTEGER,
            defense INTEGER,
            special_attack INTEGER,
            special_defense INTEGER,
            speed INTEGER,
            generation INTEGER
        )
        """)

        with open("../data/pokemon.csv", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            batch = []

            for row in reader:
                batch.append((
                    row["Name"],
                    row["Form"],
                    row["Type1"],
                    row["Type2"],
                    row["Total"],
                    row["HP"],
                    row["Attack"],
                    row["Defense"],
                    row["Sp. Atk"],
                    row["Sp. Def"],
                    row["Speed"],
                    row["Generation"],
                ))
            if len(batch) >= BATCH_SIZE:
                await db.executemany(
                    """
                    INSERT INTO pokemons (
                        name,
                        form,
                        type1,
                        type2,
                        total,
                        hp,
                        attack,
                        defense,
                        special_attack,
                        special_defense,
                        speed,
                        generation
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    batch
                )

                await db.commit()
                batch.clear()

            if batch:
                await db.executemany(
                    """
                    INSERT INTO pokemons (
                        name,
                        form,
                        type1,
                        type2,
                        total,
                        hp,
                        attack,
                        defense,
                        special_attack,
                        special_defense,
                        speed,
                        generation
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    batch
                )

                await db.commit()
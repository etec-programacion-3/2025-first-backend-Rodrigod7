from tortoise import Tortoise

async def init_db():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",  # SQLite se creará automáticamente
        modules={"models": ["app.models"]}  # Indica dónde están los modelos
    )
    await Tortoise.generate_schemas()  # Crea las tablas en la base de datos
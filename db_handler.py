import asyncpg
import os

async def init_db():
    conn = await asyncpg.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME'),
        host=os.getenv('DB_HOST')
    )
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id SERIAL PRIMARY KEY,
            data BYTEA NOT NULL
        )
    ''')
    await conn.close()

async def store_images(images):
    conn = await asyncpg.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME'),
        host=os.getenv('DB_HOST')
    )
    for img_data in images:
        await conn.execute('''
            INSERT INTO images(data) VALUES($1)
        ''', img_data)
    await conn.close()

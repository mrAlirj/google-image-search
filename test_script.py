import pytest
import asyncio
from image_downloader import download_images, resize_images
from db_handler import init_db, store_images

@pytest.mark.asyncio
async def test_download_images():
    images = await download_images("cute kittens", 5)
    assert len(images) == 5
    assert all(img is not None for img in images)

@pytest.mark.asyncio
async def test_resize_images():
    images = [b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'] * 5  # Simplified example
    resized_images = await resize_images(images)
    assert len(resized_images) == 5
    assert all(isinstance(img, bytes) for img in resized_images)

@pytest.mark.asyncio
async def test_store_images():
    await init_db()
    images = [b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'] * 5
    await store_images(images)
    # Assuming the database is fresh, we should have 5 entries.
    conn = await asyncpg.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME'),
        host=os.getenv('DB_HOST')
    )
    rows = await conn.fetch('SELECT * FROM images')
    assert len(rows) == 5
    await conn.close()

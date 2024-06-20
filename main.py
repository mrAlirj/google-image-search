import asyncio
import os
from image_downloader import download_images, resize_images
from db_handler import init_db, store_images

async def main():
    query = os.getenv("SEARCH_QUERY")
    max_images = int(os.getenv("MAX_IMAGES", 10))  # Default to 10 if not provided

    if not query:
        raise ValueError("SEARCH_QUERY environment variable is required.")

    await init_db()

    images = await download_images(query, max_images)
    resized_images = await resize_images(images)

    await store_images(resized_images)

if __name__ == "__main__":
    asyncio.run(main())

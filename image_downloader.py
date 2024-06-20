import aiohttp
import asyncio
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from urllib.parse import urljoin

async def fetch_image(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                img_data = await response.read()
                return img_data
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
    return None

async def download_images(query, max_images):
    search_url = f"https://www.google.com/search?q={query}&tbm=isch"
    headers = {"User-Agent": "Mozilla/5.0"}

    async with aiohttp.ClientSession() as session:
        async with session.get(search_url, headers=headers) as response:
            html = await response.text()

        image_urls = extract_image_urls(html, search_url)

        tasks = [fetch_image(session, url) for url in image_urls[:max_images]]
        return await asyncio.gather(*tasks)

def extract_image_urls(html, base_url):
    soup = BeautifulSoup(html, 'lxml')
    img_tags = soup.find_all('img')
    urls = [urljoin(base_url, img['src']) for img in img_tags if 'src' in img.attrs]
    return urls

async def resize_images(images, size=(128, 128)):
    resized_images = []
    for img_data in images:
        if img_data:
            image = Image.open(BytesIO(img_data))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            image = image.resize(size)
            buf = BytesIO()
            image.save(buf, format="JPEG")
            resized_images.append(buf.getvalue())
    return resized_images

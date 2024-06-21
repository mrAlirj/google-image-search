import asyncio
import aiohttp
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image


async def fetch_image(session: aiohttp.ClientSession, url: str) -> bytes | None:
    """
    Fetch an image from the given URL using an aiohttp session.

    Args:
        session (aiohttp.ClientSession): The aiohttp session to use for fetching the image.
        url (str): The URL of the image to fetch.

    Returns:
        bytes | None: The image data as bytes, or None if the fetch failed.
    """
    try:
        async with session.get(url) as response:
            if response.status == 200:
                img_data = await response.read()
                return img_data
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
    return None


async def download_images(query: str, max_images: int) -> list[bytes]:
    """
    Download images from Google Images search results for the given query.

    Args:
        query (str): The search query for Google Images.
        max_images (int): The maximum number of images to download.

    Returns:
        list[bytes]: A list of image data as bytes.
    """
    search_url = f"https://www.google.com/search?q={query}&tbm=isch"
    headers = {"User-Agent": "Mozilla/5.0"}

    async with aiohttp.ClientSession() as session:
        async with session.get(search_url, headers=headers) as response:
            html = await response.text()

        image_urls = extract_image_urls(html, search_url)

        tasks = [fetch_image(session, url) for url in image_urls[:max_images]]
        return await asyncio.gather(*tasks)


def extract_image_urls(html: str, base_url: str) -> list[str]:
    """
    Extract image URLs from the given HTML content.

    Args:
        html (str): The HTML content to extract image URLs from.
        base_url (str): The base URL to use for constructing absolute image URLs.

    Returns:
        list[str]: A list of image URLs.
    """
    soup = BeautifulSoup(html, 'lxml')
    img_tags = soup.find_all('img')
    urls = [urljoin(base_url, img['src']) for img in img_tags if 'src' in img.attrs]
    return urls


async def resize_images(images: list[bytes], size: tuple[int, int] = (128, 128)) -> list[bytes]:
    """
    Resize a list of image data as bytes to the given size.

    Args:
        images (list[bytes]): A list of image data as bytes.
        size (tuple[int, int], optional): The target size for resizing the images. Defaults to (128, 128).

    Returns:
        list[bytes]: A list of resized image data as bytes.
    """
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

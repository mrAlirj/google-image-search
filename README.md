# Image Downloader and Resizer

This repository contains a Python script that downloads images from Google search results based on a specified search query string, resizes the downloaded images, and securely stores them in a PostgreSQL database. The project utilizes asynchronous programming techniques to optimize efficiency and includes a Flask web application for viewing the stored images.

## Features

- Asynchronously download images from Google search results.
- Resize images to specified dimensions.
- Store images in a PostgreSQL database.
- Retrieve and display stored images using a Flask web application.
- Dockerized for easy deployment and encapsulation.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/your-username/image-downloader.git
cd image-downloader
```

## Environment Variables

Create a `.env` file in the root directory of the project with the following content:

```
DB_HOST=db
DB_NAME=image_db
DB_USER=user
DB_PASS=password
SEARCH_QUERY="cute kittens"
MAX_IMAGES=5
```

# Docker Setup

Ensure you have Docker and Docker Compose installed. Then, follow these steps:

    Build and Run Docker Containers


    ```bash
    docker-compose up --build
    ```

    This command will build the Docker images and start the containers. The Flask web application will be available at http://localhost:5000.

# Accessing the Application

    List Images:
    To view the list of image URLs stored in the database, visit:

    ```bash 
    http://localhost:5000/images
    ```

    View Specific Image:
    To view a specific image by its ID, visit:


    ```bash 
    http://localhost:5000/images/<id>
    ```

## File Structure

    Dockerfile: Defines the Docker image for the application.
    docker-compose.yml: Docker Compose configuration file.
    requirements.txt: Lists the Python dependencies.
    main.py: Entry point for running the image downloader script.
    image_downloader.py: Contains functions for downloading, resizing images, and extracting image URLs.
    app.py: Flask application for serving images from the database.
    test_script.py: Unit tests for the image downloader and resizer script.

## Main Scripts
`main.py`
This script is the entry point for downloading and resizing images:

```python
import asyncio
import os
from image_downloader import download_images, resize_images, store_images

async def main():
    query = os.getenv("SEARCH_QUERY", "cute kittens")
    max_images = int(os.getenv("MAX_IMAGES", 5))

    images = await download_images(query, max_images)
    resized_images = await resize_images(images)
    await store_images(resized_images)

if __name__ == "__main__":
    asyncio.run(main())
```

`image_downloader.py`
This module contains the core functionality for downloading and resizing images:

    `fetch_image(session, url)`: Fetches an image from the given URL.
    `download_images(query, max_images)`: Downloads images based on the search query.
    `extract_image_urls(html, base_url)`: Extracts image URLs from the Google search results page.
    `resize_images(images, size)`: Resizes images to the specified dimensions.
    `store_images(images)`: Stores resized images in the PostgreSQL database.

`app.py`
This is the Flask web application for viewing the stored images:

```python
from flask import Flask, send_file
import psycopg2
import io
from flask import jsonify

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST")
    )
    return conn

@app.route('/images', methods=['GET'])
def get_images():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, image_data FROM images;')
    images = cur.fetchall()
    cur.close()
    conn.close()

    image_list = [{"id": img[0], "url": f"/images/{img[0]}"} for img in images]
    return jsonify(image_list)

@app.route('/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT image_data FROM images WHERE id = %s;', (image_id,))
    image = cur.fetchone()
    cur.close()
    conn.close()

    if image is None:
        return 'Image not found!', 404

    image_data = io.BytesIO(image[0])
    return send_file(image_data, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## Running Tests

To run the unit tests, use the following command:

```bash
docker-compose run app pytest test_script.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
## License
This project is licensed under the MIT License. See the LICENSE file for details.
```css
This `README.md` file provides comprehensive documentation for your GitHub repository. It includes setup instructions, descriptions of the project's features, explanations of main scripts, information about testing, guidelines for contributing, and licensing details. Adjust the content as needed to fit your specific project requirements and preferences.
```







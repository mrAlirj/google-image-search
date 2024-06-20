from flask import Flask, send_file
import psycopg2
import io
import os
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
    cur.execute('SELECT id, data FROM images;')
    images = cur.fetchall()
    cur.close()
    conn.close()

    image_list = [{"id": img[0], "url": f"/images/{img[0]}"} for img in images]
    return jsonify(image_list)

@app.route('/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT data FROM images WHERE id = %s;', (image_id,))
    image = cur.fetchone()
    cur.close()
    conn.close()

    if image is None:
        return 'Image not found!', 404

    image_data = io.BytesIO(image[0])
    return send_file(image_data, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

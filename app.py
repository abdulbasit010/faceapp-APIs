from flask import Flask, request, jsonify,Response,send_file
from flask_cors import CORS
from flask_restful import Resource, Api
import json,glob
import os,requests
import yandex_scrapper
from urllib.parse import urlparse


# from utils import lenso_scrapper_v2
# from utils import pimeye

from werkzeug.utils import secure_filename

app = Flask(__name__)
MEGABYTE = (2 ** 10) ** 2
app.config['MAX_CONTENT_LENGTH'] = None
app.config['MAX_FORM_MEMORY_SIZE'] = 50 * MEGABYTE
api = Api(app)
CORS(app)
from uuid import uuid4
import string
import random



import cv2
import face_recognition

# ── App Setup ─────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "UploadFile")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



@app.route('/testing', methods=['GET'])
def testing():
    return json.dumps({
        'code': '200',
        'status': 'Success',
        'search_results': None,
        'message': 'Testing endpoint is working'
    })


@app.route('/search_req_similar_v1', methods=['POST'])
def search_req_similar_v1():

    if 'image' not in request.files:
        return json.dumps({
            'code': '210',
            'status': 'Error',
            'search_results': None,
            'message': 'No image file provided'
        })

    file = request.files['image']

    if file.filename == '':
        return json.dumps({
            'code': '210',
            'status': 'Error',
            'search_results': None,
            'message': 'Empty filename'
        })

    # Validate MIME type
    if not file.mimetype.startswith('image/'):
        return json.dumps({
            'code': '210',
            'status': 'Error',
            'search_results': None,
            'message': f'Invalid content type: {file.mimetype}'
        })

    # Secure filename
    original_filename = secure_filename(file.filename)
    extension = original_filename.split('.')[-1]

    # Generate random file + folder
    f_name = f"{uuid4()}.{extension}"
    letters = string.ascii_lowercase
    hash_ = ''.join(random.choice(letters) for _ in range(10))

    folder_path = os.path.join('UploadFile', hash_)
    os.makedirs(folder_path, exist_ok=True)

    filepath = os.path.join(folder_path, f_name)

    # Save file
    file.save(filepath)

    image_url = os.path.join('UploadFile', hash_, f_name)

    # Call scrapper
    resp = yandex_scrapper.get_results_similar_v2(image_url)

    return json.dumps({
        'code': '200',
        'status': 'Success',
        'search_results': resp,
        'URL': image_url,
        'filepath': filepath
    })

    name_hash = request.args.get('hash')
    file_name = request.args.get('file_name')
    if file_name and name_hash:
        folder_path = UPLOAD_FOLDER + name_hash + '/' + file_name
        path = os.path.join(folder_path)
        return send_file(path, as_attachment=True)
    else:
        message = json.dumps({"message": "Insufficient input parameters"})
        return Response(message, status=400, mimetype='application/json')







# ── Helper: Face Extraction ───────────────────────────────
def fetch_faces_from_folder(folder_path, hashh):
    files = glob.glob(os.path.join(folder_path, "*.*"))
    urls = []

    for file_path in files:
        image = face_recognition.load_image_file(file_path)
        face_locations = face_recognition.face_locations(image)

        for i, (top, right, bottom, left) in enumerate(face_locations):
            h = bottom - top
            padding = int(h * 0.2) + 5

            top = max(top - padding, 0)
            right = min(right + padding, image.shape[1])
            bottom = min(bottom + padding, image.shape[0])
            left = max(left - padding, 0)

            face_image = image[top:bottom, left:right]
            face_image_bgr = cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR)

            file_name = f"face_{i+1}.jpg"
            face_path = os.path.join(folder_path, file_name)

            cv2.imwrite(face_path, face_image_bgr)

            url = request.root_url + f"download-file?hash={hashh}&file_name={file_name}"
            urls.append(url)

    return urls


# ── Route: Fetch Faces ────────────────────────────────────
@app.route('/fetch-faces', methods=['POST'])
def fetch_faces():
    file = request.files.get('file')
    url = request.form.get('url')
    hashh = request.form.get('hash')

    if not file and not url:
        return jsonify({'error': 'Provide either file or url'}), 400

    # Create folder
    if hashh:
        folder_path = os.path.join(UPLOAD_FOLDER, hashh)
        os.makedirs(folder_path, exist_ok=True)
    else:
        hashh = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        folder_path = os.path.join(UPLOAD_FOLDER, hashh)
        os.makedirs(folder_path)

    # Save file
    if file:
        ext = os.path.splitext(file.filename)[1]
        file_name = str(uuid4()) + ext
        file_path = os.path.join(folder_path, file_name)
        file.save(file_path)

    elif url:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            ext = ".jpg"
            content_type = response.headers.get("Content-Type", "")

            if "png" in content_type:
                ext = ".png"
            elif "webp" in content_type:
                ext = ".webp"

            file_name = str(uuid4()) + ext
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, "wb") as f:
                f.write(response.content)

        except Exception as e:
            return jsonify({'error': f'Failed to download image: {str(e)}'}), 400

    # Extract faces
    face_urls = fetch_faces_from_folder(folder_path, hashh)

    return jsonify({
        "face_count": len(face_urls),
        "hash": hashh,
        "file_name": file_name,
        "faceURLs": face_urls
    })


# ── Route: Download Face ──────────────────────────────────
@app.route('/download-file', methods=['GET'])
def download_file():
    hashh = request.args.get('hash')
    file_name = request.args.get('file_name')

    if not hashh or not file_name:
        return jsonify({"error": "Missing parameters"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, hashh, file_name)
    return send_file(file_path, as_attachment=True)


# # ── Run ──────────────────────────────────────────────────
# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=5000)




# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))  # default to 5000 if PORT is not set
#     app.run(host="0.0.0.0", port=port)
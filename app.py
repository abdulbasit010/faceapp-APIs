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

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))  # default to 5000 if PORT is not set
#     app.run(host="0.0.0.0", port=port)
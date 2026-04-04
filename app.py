from flask import Flask, request, jsonify,Response,send_file
from flask_cors import CORS
from flask_restful import Resource, Api
import json,glob
import os,requests
import yandex_scrapper
from urllib.parse import urlparse


import face_recognition
from PIL import Image
import pillow_heif

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



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "UploadFile")

# Ensure folder exists
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

@app.route('/')
def home():
    return "Running"

@app.route('/fetch-faces', methods=['POST'])
def fetch_faces():
    """ Fetches faces from a given URL and returns the results.
    """
    if request.method == 'POST':
        file = request.files['file']
        hashh = request.form['hash']
        # type_ = request.form['file_type']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid4()) + extension
        if hashh:
            folder_path = UPLOAD_FOLDER + hashh
            file.save(os.path.join(folder_path, f_name))
        else:
            letters = string.ascii_lowercase
            hash_ = ''.join(random.choice(letters) for i in range(10))
            hashh = hash_
            folder_path = UPLOAD_FOLDER + hash_
            os.mkdir(folder_path)
            file.save(os.path.join(folder_path, f_name))
            
        faceURLS = fetch_facesfromURL(folder_path, hashh)
        return jsonify({'face_count': len(faceURLS),'hash': hashh,'file_name': f_name, 'faceURLs': faceURLS})

def fetch_facesfromURL(folder_path, hashh):
    """ Fetches faces from a given URL and returns the results.
    """
    filess = glob.glob(os.path.join(folder_path)+'/*.*')
    import cv2
    urls= []
    for filee in filess:
        image = cv2.imread(filee)
        # Load the image
        padding = 100
        if filee.lower().endswith(('.heic', '.heif')):
            pillow_heif.register_heif_opener()
            heif_file = pillow_heif.read_heif(filee)
            image_pil = Image.frombytes(
                heif_file.mode, 
                heif_file.size, 
                heif_file.data
            )
            temp_jpg = filee + ".jpg"
            image_pil.save(temp_jpg, "JPEG")
            filee = temp_jpg  # Update path for face_recognition
        
        image = face_recognition.load_image_file(filee)

        # Detect face locations
        face_locations = face_recognition.face_locations(image)

        # Ensure output directory exists
        # os.makedirs(output_dir, exist_ok=True)

        # Loop through each detected face
        for i, (top, right, bottom, left) in enumerate(face_locations):
            # Add padding to include hair (clamp to image dimensions)
            print('top:'+str(top)+' bottom:'+str(bottom))
            h = bottom - top
            w = right - left
            padding = round(h*0.2) + 5
            top = max(top - padding, 0)
            right = min(right + padding, image.shape[1])
            bottom = min(bottom + padding, image.shape[0])
            left = max(left - padding, 0)

            # Crop the face + padding region
            face_image = image[top:bottom, left:right]

            # Convert RGB (face_recognition uses RGB, OpenCV uses BGR)
            face_image_bgr = cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR)
    
            # Save the cropped face
            file_name = f"face_{i+1}.jpg"
            face_filename = os.path.join(folder_path, f"face_{i+1}.jpg")
            cv2.imwrite(face_filename, face_image_bgr)
            files_url = request.root_url + f'/download-file?hash={hashh}&file_name='+file_name
            urls.append(files_url)
    
    return urls

@app.route('/download-file', methods=['GET'])
def download_file(*args):
    name_hash = request.args.get('hash')
    file_name = request.args.get('file_name')
    if file_name and name_hash:
        folder_path = UPLOAD_FOLDER + name_hash + '/' + file_name
        path = os.path.join(folder_path)
        return send_file(path, as_attachment=True)
    else:
        message = json.dumps({"message": "Insufficient input parameters"})
        return Response(message, status=400, mimetype='application/json')


# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))  # default to 5000 if PORT is not set
#     app.run(host="0.0.0.0", port=port)
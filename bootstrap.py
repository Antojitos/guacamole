import os
import hashlib
import uuid

from flask import Flask, request, redirect, url_for, json
from flask.ext.pymongo import PyMongo
from werkzeug import secure_filename

app = Flask(__name__)

app.debug = True

UPLOAD_FOLDER = './files/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

MONGO_HOST = '10.0.3.7'
app.config['MONGO_HOST'] = MONGO_HOST
mongo = PyMongo(app)

def file_extension(filename):
    return filename.rsplit('.', 1)[1]

def allowed_file(filename):
    return '.' in filename and \
           file_extension(filename) in ALLOWED_EXTENSIONS

def hash_file(file):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    buffer = file.read(BLOCKSIZE)
    while len(buffer) > 0:
        hasher.update(buffer)
        buffer = file.read(BLOCKSIZE)
    return hasher.hexdigest()

def save_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_uuid = uuid.uuid1().urn[9:]
        file_sharding = file_uuid.split('-')
        file_path_list = [app.config['UPLOAD_FOLDER']] + file_sharding + [filename]
        file_path = os.path.join(*file_path_list)
        
        parent_path = os.path.dirname(file_path)
        if not os.path.exists(parent_path):
            os.makedirs(parent_path)
        file.save(file_path)

        meta = {
            'uuid': file_uuid,
            'name':filename,
            'path': file_path,
            'sha224': hash_file(file)
            # mime-type
            # keywords
        }

        # instance = mongo.db.files.insert_one(file_meta)
        
        # return instance
        return meta

@app.route('/files/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_file = save_file(request.files['file'])
        return json.jsonify(new_file)

    if request.method == 'GET':
        files = mongo.db.files.find()
        return json.jsonify(files)

@app.route('/files/<int:file_id>', methods=['GET'])
def get_file(file_id):
    return mongo.db.files.find_one({'id': file_id})


if __name__ == '__main__':
    app.run()

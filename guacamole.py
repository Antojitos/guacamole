import os
import string
import random
import hashlib
import datetime
import mimetypes

from bson.json_util import dumps

from flask import Flask, request, send_from_directory
from flask.ext.pymongo import PyMongo
from werkzeug import secure_filename

# CONF

HOST = '0.0.0.0'
PORT= 5000
UPLOAD_FOLDER = './files/'
SHARD_CHARS = string.letters + string.digits
SHARD_NUMBER = 6
SHARD_SIZE = 4
HASH_BLOCKSIZE = 65536
TAGS_SEPARATOR = ','

# INIT

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mimetypes.init()
mongo = PyMongo(app)

# METHODS

def hash_file(file):
    return hashlib.sha1(file.read()).hexdigest()

def get_shard_path():
    shard = ''.join((random.choice(SHARD_CHARS)) for x in range(SHARD_NUMBER * SHARD_SIZE))
    shard = [shard[i:i+SHARD_SIZE] for i in range(0, len(shard), SHARD_SIZE)]
    return os.path.join(*shard)

def get_file_size(file):
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    return file_size

def get_tags(tags_string):
    tags = [tag.strip().lower() for tag in tags_string.split(TAGS_SEPARATOR)]
    return tags

def save_file():
    file = request.files['file']
    tags = get_tags(request.form['tags'])

    filename = secure_filename(file.filename)
    shard_path = get_shard_path()
    file_uri = os.path.join(shard_path, filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_uri)
    file_folder = os.path.dirname(file_path)
    
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)

    file.save(file_path)

    file_meta = {
        'sha1': hash_file(file),
        'name':filename,
        'uri': file_uri,
        'create_date': datetime.datetime.utcnow(),
        'mime_type': mimetypes.guess_type(file_path)[0],
        'size': get_file_size(file)
    }

    if tags:
       file_meta['tags'] = tags

    mongo.db.files.insert_one(file_meta)
    return file_meta

# ROUTES

@app.route('/files/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_file = save_file()
        return dumps(new_file)

    if request.method == 'GET':
        files = mongo.db.files.find()
        return dumps(files)

@app.route('/files/<path:file_uri>', methods=['GET'])
def get_file_data(file_uri):
    return send_from_directory(app.config['UPLOAD_FOLDER'], file_uri)

@app.route('/files/<path:file_uri>/meta', methods=['GET'])
def get_file(file_uri):
    item = mongo.db.files.find_one({'uri': file_uri})
    return dumps(item)

# START!

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)

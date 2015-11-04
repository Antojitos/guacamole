from flask import request, send_from_directory
from bson.json_util import dumps
from guacamole import app
from guacamole.models import File

@app.route('/files/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        item = File(
            file=request.files['file'],
            tags=request.form['tags'])
        item.save()
        return dumps(item.get_meta())

    if request.method == 'GET':
        files = File.find()
        return dumps(files)

@app.route('/files/<path:file_uri>', methods=['GET'])
def get_file_data(file_uri):
    return send_from_directory(app.config['UPLOAD_DIR'], file_uri)

@app.route('/files/<path:file_uri>/meta', methods=['GET'])
def get_file(file_uri):
    item = File.find_one({'uri': file_uri})
    return dumps(item)
